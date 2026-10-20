"""Assembly preview PNGs for the puppet base.

Poses the parts with CadQuery (build_puppet_base.assemble), writes coarse STLs, then renders them.
Engine: VTK off-screen (z-buffered, proper lighting) if it works on this machine, otherwise matplotlib + trimesh.
The engine that was actually used is printed at the end and written into the PNG's title strip.

    .venv\\Scripts\\python.exe render_preview.py            # writes out/preview_rest.png, out/preview_bobbed_tilted.png,
                                                            # out/preview_with_cloud.png
    .venv\\Scripts\\python.exe render_preview.py claude     # only out/preview_claude.png (Clawd shell on the base, two poses)
"""
import os
import sys
import math

import build_puppet_base as B

OUT = B.OUT_DIR
POSE_DIR = os.path.join(OUT, "_assembly", "_pose")

COLORS = {
    "base": (0.62, 0.62, 0.66), "turntable": (0.25, 0.45, 0.80), "column": (0.70, 0.78, 0.90),
    "carriage": (0.95, 0.55, 0.15), "yoke": (0.85, 0.20, 0.20), "lever": (0.85, 0.20, 0.20),
    "neck_A": (0.25, 0.65, 0.35), "neck_B": (0.45, 0.80, 0.45), "neck_C": (0.15, 0.50, 0.30),
    "head": (0.96, 0.90, 0.78), "socket": (0.60, 0.35, 0.75), "horn": (0.95, 0.80, 0.15),
    "wire": (0.20, 0.20, 0.20), "cloud": (0.80, 0.90, 1.00), "claude": (0.85, 0.47, 0.34), "softlegs": (0.85, 0.47, 0.34),
}
OPACITY = {"column": 0.35, "cloud": 0.55, "softlegs": 0.45}


def color_key(name):
    name = name.split(":")[-1]                     # "rest:base_L" -> "base_L" (several poses in one picture)
    if name.startswith("claude_legs"):             # Clawd's soft legs (sewn fleece, not printed): drawn see-through
        return "softlegs"
    for k in ("base", "turntable", "column", "carriage", "yoke", "lever", "neck_A", "neck_B", "neck_C", "head",
              "socket", "horn", "wire", "cloud", "claude"):
        if name.startswith(k):
            return k
    return "base"


def write_pose(P, tag, **pose):
    d = os.path.join(POSE_DIR, tag)
    os.makedirs(d, exist_ok=True)
    A = B.assemble(P, **pose)
    paths = {}
    for k, wp in A.items():
        p = os.path.join(d, k + ".stl")
        B.export_stl(wp, p, tol=0.12, ang=0.35)
        paths[k] = p
    return paths


def render_vtk(paths, png, title, size=(1300, 1700), az=38, el=14, hide=(), focal=(0, 0, 165), dist=900, front=False):
    """front=True puts the camera on the +Y (face) side instead of the back. focal / dist / size only matter for the Claude picture;
    the defaults reproduce the original three previews exactly."""
    import vtk
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    ren.SetBackground2(0.88, 0.92, 0.97)
    ren.GradientBackgroundOn()
    for name, p in paths.items():
        if name in hide:
            continue
        r = vtk.vtkSTLReader()
        r.SetFileName(p)
        r.Update()
        norm = vtk.vtkPolyDataNormals()
        norm.SetInputConnection(r.GetOutputPort())
        norm.SetFeatureAngle(50)
        norm.Update()
        m = vtk.vtkPolyDataMapper()
        m.SetInputConnection(norm.GetOutputPort())
        a = vtk.vtkActor()
        a.SetMapper(m)
        key = color_key(name)
        a.GetProperty().SetColor(*COLORS[key])
        a.GetProperty().SetOpacity(OPACITY.get(key, 1.0))
        a.GetProperty().SetSpecular(0.25)
        ren.AddActor(a)
    txt = vtk.vtkTextActor()
    txt.SetInput(title)
    txt.GetTextProperty().SetFontSize(26)
    txt.GetTextProperty().SetColor(0.1, 0.1, 0.15)
    txt.SetPosition(24, size[1] - 48 - 30 * title.count("\n"))      # a second title line grows upwards, so start lower
    ren.AddViewProp(txt)
    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.SetSize(*size)
    win.SetMultiSamples(4)
    win.AddRenderer(ren)
    cam = ren.GetActiveCamera()
    cam.SetViewUp(0, 0, 1)
    cam.SetFocalPoint(*focal)
    cam.SetPosition(focal[0], focal[1] + (dist if front else -dist), focal[2])
    cam.Azimuth(az)
    cam.Elevation(el)
    cam.SetViewAngle(24)
    ren.ResetCameraClippingRange()
    win.Render()
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(win)
    w2i.Update()
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(png)
    wr.SetInputConnection(w2i.GetOutputPort())
    wr.Write()
    return "VTK off-screen"


def render_mpl(paths, png, title, size=(1300, 1700), az=38, el=14, hide=()):
    import numpy as np
    import trimesh
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    tris, cols = [], []
    light = np.array([0.4, -0.6, 0.7])
    light /= np.linalg.norm(light)
    for name, p in paths.items():
        if name in hide:
            continue
        m = trimesh.load(p, force="mesh")
        key = color_key(name)
        base = np.array(COLORS[key])
        n = m.face_normals
        shade = 0.45 + 0.55 * np.clip(n @ light, 0, 1)
        tris.append(m.triangles)
        cols.append(np.clip(base[None, :] * shade[:, None], 0, 1))
    tris = np.concatenate(tris)
    cols = np.concatenate(cols)
    fig = plt.figure(figsize=(size[0] / 100, size[1] / 100), dpi=100)
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection3d(Poly3DCollection(tris, facecolors=cols, edgecolors="none", linewidths=0))
    ax.set_xlim(-170, 170)
    ax.set_ylim(-170, 170)
    ax.set_zlim(0, 340)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=el + 6, azim=az - 90)
    ax.set_axis_off()
    fig.suptitle(title, x=0.03, y=0.97, ha="left", fontsize=18)
    fig.savefig(png, facecolor="white")
    plt.close(fig)
    return "matplotlib + trimesh"


def main():
    P = B.build_all()
    os.makedirs(OUT, exist_ok=True)
    poses = [
        ("rest", "preview_rest.png", "Puppet base: at rest (carriage down, head level, arms down)",
         dict(bob=0.0, nod=0.0, tilt=0.0, arm_deg=-90.0, with_cloud=False)),
        ("bobbed", "preview_bobbed_tilted.png",
         "Puppet base: bobbed up 34 mm, head nodded 20 and tilted 20 degrees, arms raised",
         dict(bob=B.BOB_THROW, nod=20.0, tilt=20.0, arm_deg=35.0, with_cloud=False)),
        ("cloud", "preview_with_cloud.png", "Puppet base with the example cloud former on the head (head level)",
         dict(bob=0.0, nod=0.0, tilt=0.0, arm_deg=-90.0, with_cloud=True)),
    ]
    engine = None
    for tag, png, title, pose in poses:
        paths = write_pose(P, tag, **pose)
        out_png = os.path.join(OUT, png)
        try:
            engine = render_vtk(paths, out_png, title)
        except Exception as e:  # fall back to matplotlib
            print("VTK render failed (", repr(e)[:200], ") - using matplotlib", flush=True)
            engine = render_mpl(paths, out_png, title)
        print(f"{out_png}  ({os.path.getsize(out_png) / 1e3:.0f} KB)", flush=True)
    print("render engine:", engine)


def main_claude():
    """out/preview_claude.png: the Clawd (Claude) shell on the whole base, seen from the front (face side), two poses side by side:
    at rest (left) and bobbed up, nodded 20 and tilted 20 (right). No arms are fitted on the round characters, so the arm horns
    and wires are left out. Clawd's four legs are sewn soft fleece, not printed, so they are drawn see-through under the body."""
    import build_shells as S
    P = B.build_all()
    L, R = S.build_claude()
    legs = S.clawd_soft_legs()
    DX = 130.0                                      # seen from the front +X is on the left of the picture: rest goes to +X
                                                    # (Clawd with its stub arms is 196 wide, so the two poses sit 260 apart)
    poses = [("rest", DX, dict(bob=0.0, nod=0.0, tilt=0.0)),
             ("bobbed", -DX, dict(bob=B.BOB_THROW, nod=20.0, tilt=20.0))]
    paths = {}
    for tag, dx, pose in poses:
        d = os.path.join(POSE_DIR, "claude_" + tag)
        os.makedirs(d, exist_ok=True)
        A = B.assemble(P, arm_deg=-90.0, **pose)
        parts = {k: v for k, v in A.items() if not k.startswith(("horn", "wire"))}
        parts["claude_L"] = S.pose_head_frame(L, **pose)
        parts["claude_R"] = S.pose_head_frame(R, **pose)
        parts["claude_legs"] = S.pose_head_frame(legs, **pose)
        for k, wp in parts.items():
            p = os.path.join(d, k + ".stl")
            B.export_stl(wp.translate((dx, 0, 0)), p, tol=0.12, ang=0.35)
            paths[tag + ":" + k] = p
    png = os.path.join(OUT, "preview_claude.png")
    title = ("Clawd shell on the full base. Left: at rest. Right: bobbed up 34 mm, nodded 20 and tilted 20 degrees "
             "(seen from the front, no arms fitted).\nThe four see-through legs are soft sewn fleece, not printed.")
    render_vtk(paths, png, title, size=(2000, 1500), az=-22, el=4, focal=(0, 0, 190), dist=1150, front=True)
    print(f"{png}  ({os.path.getsize(png) / 1e3:.0f} KB)")


if __name__ == "__main__":
    if "claude" in sys.argv[1:]:
        main_claude()
    else:
        main()
