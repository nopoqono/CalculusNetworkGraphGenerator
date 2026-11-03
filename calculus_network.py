"""
calculus_network.py

An aesthetic, constellation-style interactive network graph linking key concepts,
formulas, and theorems across Calculus 1, Calculus 2, and Calculus 3.

Features:
- Spatial galaxy clustering with sweeping translucent curved filaments
- KaTeX mathematical typesetting with architectural formula breakdowns
- Interactive Guided Thread Stepper (Prev / Next camera focus)
- Dual visual theme: Reference Constellation Mode (White/Crimson on Pitch Black)
  and Course Color Mode (Calc 1 Blue, Calc 2 Green, Calc 3 Pink)
"""

import json
import networkx as nx
from pyvis.network import Network


# ==============================================================================
# 1. Visual Themes & Course Color Configuration
# ==============================================================================
COURSE_COLORS = {
    "Calculus 1": "#AFC9E8",  # Foundations (Blue)
    "Calculus 2": "#B9D7C2",  # Techniques & Series (Green)
    "Calculus 3": "#E7B8C8",  # Multivariable & Vector Fields (Pink)
}

# Core mathematical threads for guided step-by-step follow-through
THREADS = {
    "thread_1": {
        "name": "Thread 1: Fundamental Theorem Chain",
      "color": "#D9959E",
        "sequence": [
            "FTC",
            "FTLI",
            "Greens_Theorem",
            "Stokes_Theorem",
            "Divergence_Theorem",
        ],
    },
    "thread_2": {
        "name": "Thread 2: Derivative & Rate of Change Chain",
      "color": "#86C9BE",
        "sequence": [
            "Limits_Continuity",
            "Single_Derivative",
            "Partial_Derivatives",
            "Gradient",
            "Directional_Derivative",
            "Tangent_Plane",
            "Lagrange_Multipliers",
        ],
    },
    "thread_3": {
        "name": "Thread 3: Integration & Coordinate Transformation",
      "color": "#DCC58E",
        "sequence": [
            "Definite_Integral",
            "U_Substitution",
            "Integration_By_Parts",
            "Trig_Sub",
            "Polar_Coordinates",
            "Double_Integral",
            "Triple_Integral",
            "Cylindrical_Spherical",
            "Jacobian",
        ],
    },
    "thread_4": {
        "name": "Thread 4: Vectors & Multivariable Geometry",
      "color": "#B6A1CB",
        "sequence": [
            "Parametric_Curves",
            "Vectors_2D_3D",
            "Dot_Product",
            "Cross_Product",
            "Lines_And_Planes",
            "Quadric_Surfaces",
        ],
    },
}

WORKED_EXAMPLES = {
    "Greens_Theorem": {
      "problem": r"Let $\mathbf{F}(x,y)=\langle -y/2, x/2\rangle$ and let $C$ be the unit circle traversed counterclockwise. Evaluate $\oint_C \mathbf{F}\cdot d\mathbf{r}$.",
      "steps": [
        {
          "title": "Identify the field and boundary",
          "focus": "Parametric_Curves",
          "prerequisites": ["Vectors_2D_3D"],
          "explanation": "Write the field as P = -y/2 and Q = x/2. The boundary is the unit circle with positive (counterclockwise) orientation, so it encloses the unit disk D.",
          "latex": r"\mathbf{F}=\langle P,Q\rangle=\left\langle -\frac{y}{2},\frac{x}{2}\right\rangle,\qquad C:\ x^2+y^2=1",
        },
        {
          "title": "Compute the scalar curl",
          "focus": "Partial_Derivatives",
          "prerequisites": ["Single_Derivative"],
          "explanation": "Differentiate Q with respect to x and P with respect to y, holding the other variable constant. Their difference is the constant curl 1.",
          "latex": r"\frac{\partial Q}{\partial x}=\frac{1}{2},\qquad \frac{\partial P}{\partial y}=-\frac{1}{2},\qquad Q_x-P_y=1",
        },
        {
          "title": "Integrate over the disk",
          "focus": "Double_Integral",
          "prerequisites": ["Polar_Coordinates"],
          "explanation": "The integrand is 1 throughout D. Polar coordinates describe the unit disk with 0 <= r <= 1 and 0 <= theta <= 2 pi, so the double integral is its area.",
          "latex": r"\iint_D 1\,dA=\int_0^{2\pi}\int_0^1 r\,dr\,d\theta=\pi",
        },
        {
          "title": "Apply Green's Theorem",
          "focus": "Greens_Theorem",
          "prerequisites": ["Double_Integral", "Line_Integral"],
          "explanation": "Green's Theorem equates the counterclockwise boundary circulation to the double integral of Q_x - P_y over D. Substituting the result gives the requested circulation.",
          "latex": r"\oint_C P\,dx+Q\,dy=\iint_D(Q_x-P_y)\,dA=\iint_D1\,dA=\boxed{\pi}",
        },
        {
          "title": "Check with a direct line integral",
          "focus": "Line_Integral",
          "prerequisites": ["Parametric_Curves"],
          "explanation": "Parameterize the circle by r(t) = (cos t, sin t), 0 <= t <= 2 pi. Then F(r(t)) dot r'(t) = 1/2, whose integral is pi, confirming the theorem's result.",
          "latex": r"\mathbf{r}(t)=\langle\cos t,\sin t\rangle,\qquad \mathbf{F}(\mathbf{r}(t))\cdot\mathbf{r}'(t)=\frac{1}{2},\qquad \int_0^{2\pi}\frac{1}{2}\,dt=\pi",
        },
      ],
    }
  }


def make_tooltip(
    node_id: str,
    label: str,
    category: str,
    latex_formula: str,
    architecture: list[tuple[str, str]],
    description: str,
    badge_code: str = "",
) -> str:
    """
    Generates an architecturally structured HTML hover card with KaTeX formula
    rendering and a modular breakdown of mathematical components.
    """
    color = COURSE_COLORS.get(category, "#FFFFFF")
    arch_rows = "".join(
        f"<div style='display:flex; justify-content:space-between; gap:12px; "
        f"padding:4px 0; border-bottom:1px solid rgba(86,100,122,0.14); font-size:11.5px;'>"
        f"<span style='color:#687589; font-weight:600; white-space:nowrap;'>{role}</span>"
        f"<span class='katex-inline' style='color:#384455; text-align:right;'>{spec}</span>"
        f"</div>"
        for role, spec in architecture
    )
    badge_html = (
        f"<span style='background:#d9959e; color:#384455; padding:2px 6px; "
        f"border-radius:3px; font-size:10px; font-family:monospace; font-weight:700;'>"
        f"{badge_code}</span>"
        if badge_code
        else ""
    )

    return (
        f"<div class='calc-tooltip-card' style='width:380px; font-family:Inter, Segoe UI, sans-serif; "
        f"background:rgba(255, 255, 255, 0.97); color:#384455; padding:14px; "
        f"border:1px solid rgba(86,100,122,0.22); border-left:4px solid {color}; "
        f"border-radius:8px; box-shadow:0 12px 32px rgba(72,82,102,0.18);'>"
        f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>"
        f"<span style='font-size:10.5px; text-transform:uppercase; letter-spacing:1.2px; "
        f"color:{color}; font-weight:700;'>{category}</span>"
        f"{badge_html}"
        f"</div>"
        f"<div style='font-size:15px; font-weight:700; color:#384455; margin-bottom:8px;'>{label}</div>"
        f"<div class='katex-display-box' data-latex=\"{latex_formula}\" "
        f"style='margin:8px 0; padding:10px 12px; background:#f7f8fb; "
        f"border:1px solid rgba(86,100,122,0.16); border-radius:6px; "
        f"color:#65738a; font-size:13.5px; text-align:center; overflow-x:auto;'>"
        f"$${latex_formula}$$"
        f"</div>"
        f"<div style='margin:8px 0; background:rgba(230,235,243,0.55); padding:6px 10px; border-radius:6px;'>"
        f"<div style='font-size:10px; text-transform:uppercase; letter-spacing:0.8px; color:#bd7884; "
        f"font-weight:700; margin-bottom:4px;'>Formula Architecture</div>"
        f"{arch_rows}"
        f"</div>"
        f"<div style='font-size:12px; line-height:1.5; color:#526074; margin-top:8px;'>"
        f"{description}"
        f"</div>"
        f"</div>"
    )


# ==============================================================================
# 2. Graph Data Definition with Spatial Constellation Coordinates
# ==============================================================================
def build_calculus_digraph() -> tuple[nx.DiGraph, dict]:
    """
    Constructs a directed NetworkX graph with spatial coordinates grouped into
    three distinct constellation clusters:
      - Cluster 1 (Bottom-Left): Calculus 1 Foundations
      - Cluster 2 (Top-Left): Calculus 2 Techniques & Series
      - Cluster 3 (Right Macro-Galaxy): Calculus 3 Multivariable & Vector Fields
    """
    G = nx.DiGraph()
    node_metadata = {}

    # Each tuple:
    # (id, label, group, latex_formula, architecture_list, description, size, x, y, hub_badge)
    nodes_data = [
        # ======================================================================
        # CLUSTER 1: CALCULUS 1 (Bottom-Left Constellation around x=-950, y=380)
        # ======================================================================
        (
            "Limits_Continuity",
            "Limits & Continuity",
            "Calculus 1",
            r"\lim_{x \to a} f(x) = L \iff \forall \varepsilon > 0, \exists \delta > 0",
            [
                ("Input Approach", r"$0 < |x - a| < \delta$"),
                ("Output Tolerance", r"$|f(x) - L| < \varepsilon$"),
                ("Continuity Condition", r"$\lim_{x \to a} f(x) = f(a)$"),
            ],
            "Establishes the local behavior of a function near a target point and guarantees unbroken graph behavior across an interval.",
            20,
            -1180,
            480,
            "",
        ),
        (
            "Single_Derivative",
            "Single-Variable Derivative",
            "Calculus 1",
            r"f'(x) = \frac{df}{dx} = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            [
                ("Secant Difference", r"$\Delta f = f(x+h) - f(x)$"),
                ("Differential Step", r"$h = \Delta x \to 0$"),
                ("Geometric Meaning", r"Slope of tangent line at $x$"),
            ],
            "Measures the instantaneous rate of change of a single-variable function by shrinking a secant slope to a tangent point.",
            28,
            -980,
            340,
            "1.104192",
        ),
        (
            "Chain_Rule",
            "Chain Rule",
            "Calculus 1",
            r"\frac{d}{dx}\bigl[f(g(x))\bigr] = f'(g(x)) \cdot g'(x)",
            [
                ("Outer Rate", r"$df / dg = f'(g(x))$"),
                ("Inner Rate", r"$dg / dx = g'(x)$"),
                ("Composition Product", r"$\frac{df}{dg} \cdot \frac{dg}{dx}$"),
            ],
            "Propagates rates of change through nested composite functions by multiplying outer and inner derivatives.",
            19,
            -1150,
            230,
            "",
        ),
        (
            "Optimization_1D",
            "1D Optimization",
            "Calculus 1",
            r"f'(c) = 0, \quad f''(c) < 0 \implies \text{Local Max}",
            [
                ("Stationary Condition", r"$f'(c) = 0 \text{ or undefined}$"),
                ("Concavity Test", r"$f''(c) > 0 \text{ (Min)}, < 0 \text{ (Max)}$"),
                ("Output", r"Extrema $(c, f(c))$"),
            ],
            "Locates peaks and valleys of a 1D curve where the instantaneous slope flattens to zero.",
            18,
            -840,
            540,
            "",
        ),
        (
            "Definite_Integral",
            "Single Definite Integral",
            "Calculus 1",
            r"\int_{a}^{b} f(x)\,dx = \lim_{n \to \infty} \sum_{i=1}^{n} f(x_i^*)\,\Delta x",
            [
                ("Interval Domain", r"$x \in [a, b], \quad \Delta x = \frac{b-a}{n}$"),
                ("Riemann Slice", r"$\text{Height } f(x_i^*) \times \text{Width } \Delta x$"),
                ("Accumulated Output", r"Net signed area under $f(x)$"),
            ],
            "Accumulates an infinite number of infinitesimal rectangular slices to compute exact net signed area over [a, b].",
            28,
            -920,
            190,
            "",
        ),
        (
            "FTC",
            "Fundamental Theorem of Calculus",
            "Calculus 1",
            r"\int_{a}^{b} F'(x)\,dx = F(b) - F(a)",
            [
                ("Interior Accumulation", r"$\int_a^b F'(x)\,dx$ over $[a,b]$"),
                ("Antiderivative", r"$F(x)$ such that $F'(x) = f(x)$"),
                ("Boundary Evaluation", r"Endpoints $F(b) - F(a)$"),
            ],
            "The foundational bridge of calculus: converts global accumulation of derivatives across an interval into a simple evaluation at its boundary endpoints.",
            34,
            -740,
            340,
            "6.695920",
        ),
        (
            "U_Substitution",
            "U-Substitution",
            "Calculus 1",
            r"\int_{a}^{b} f(g(x))\,g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du",
            [
                ("Coordinate Map", r"$u = g(x)$"),
                ("1D Jacobian Scaling", r"$du = g'(x)\,dx$"),
                ("Transformed Bounds", r"$[a, b] \mapsto [g(a), g(b)]$"),
            ],
            "Reverses the Chain Rule to simplify integrals by stretching or compressing the 1D coordinate axis.",
            21,
            -780,
            150,
            "",
        ),

        # ======================================================================
        # CLUSTER 2: CALCULUS 2 (Top-Left Constellation around x=-680, y=-340)
        # ======================================================================
        (
            "Integration_By_Parts",
            "Integration by Parts",
            "Calculus 2",
            r"\int u\,dv = u\,v - \int v\,du",
            [
                ("Differentiated Factor", r"$u \implies du = u'(x)\,dx$ (LIATE)"),
                ("Integrated Factor", r"$dv \implies v = \int dv$"),
                ("Product Rule Inverse", r"$d(uv) = u\,dv + v\,du$"),
            ],
            "Reverses the product rule to integrate products of logarithmic, inverse trig, algebraic, trigonometric, and exponential functions.",
            26,
            -780,
            -260,
            "7.403283",
        ),
        (
            "Trig_Sub",
            "Trigonometric Substitution",
            "Calculus 2",
            r"\sqrt{a^2 - x^2} \xrightarrow{x = a\sin\theta} a\cos\theta, \quad dx = a\cos\theta\,d\theta",
            [
                ("Radical Form", r"$\sqrt{a^2-x^2},\ \sqrt{a^2+x^2},\ \sqrt{x^2-a^2}$"),
                ("Trig Identity", r"$1-\sin^2\theta = \cos^2\theta,\ 1+\tan^2\theta=\sec^2\theta$"),
                ("Differential Map", r"$dx = a\cos\theta\,d\theta$"),
            ],
            "Replaces algebraic radicals with right-triangle trigonometric identities so square roots collapse into clean trig powers.",
            22,
            -600,
            -390,
            "",
        ),
        (
            "Partial_Fractions",
            "Partial Fractions",
            "Calculus 2",
            r"\frac{P(x)}{(x-a)(x^2+bx+c)} = \frac{A}{x-a} + \frac{Bx+C}{x^2+bx+c}",
            [
                ("Rational Input", r"$P(x)/Q(x)$ with $\deg(P) < \deg(Q)$"),
                ("Linear Term", r"$\int \frac{A}{x-a}\,dx = A\ln|x-a|$"),
                ("Quadratic Term", r"Yields $\ln$ and $\arctan$ primitives"),
            ],
            "Decomposes complex rational functions into simpler fractional building blocks that integrate directly into logarithms and arctangents.",
            19,
            -890,
            -420,
            "",
        ),
        (
            "Parametric_Curves",
            "Parametric Curves",
            "Calculus 2",
            r"\mathbf{r}(t) = \bigl(x(t),\,y(t)\bigr), \quad ds = \sqrt{[x'(t)]^2 + [y'(t)]^2}\,dt",
            [
                ("Parameter", r"Independent time/angle variable $t \in [a,b]$"),
                ("Velocity Tangent", r"$\mathbf{r}'(t) = \langle x'(t), y'(t) \rangle$"),
                ("Arc Length Element", r"$ds = \|\mathbf{r}'(t)\|\,dt$"),
            ],
            "Frees curves from the vertical-line test by expressing each spatial coordinate as an independent function of parameter t.",
            22,
            -520,
            -190,
            "",
        ),
        (
            "Polar_Coordinates",
            "Polar Coordinates",
            "Calculus 2",
            r"x = r\cos\theta, \quad y = r\sin\theta, \quad dA = r\,dr\,d\theta",
            [
                ("Radial Distance", r"$r = \sqrt{x^2 + y^2} \ge 0$"),
                ("Azimuth Angle", r"$\theta = \arctan(y/x) \in [0, 2\pi]$"),
                ("Polar Area Wedge", r"$dA = r\,dr\,d\theta$"),
            ],
            "Maps the 2D plane via radial distance and rotation angle, turning circular and rotational boundaries into constant intervals.",
            26,
            -440,
            -350,
            "",
        ),
        (
            "Taylor_Series",
            "Taylor & Maclaurin Series",
            "Calculus 2",
            r"f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x - a)^n",
            [
                ("Center Point", r"Expansion anchor $x = a$"),
                ("Derivative Weights", r"$c_n = f^{(n)}(a) / n!$"),
                ("Polynomial Basis", r"Power terms $(x - a)^n$"),
            ],
            "Reconstructs smooth transcendental functions as infinite polynomials governed entirely by higher-order derivatives at a single point.",
            20,
            -730,
            -510,
            "",
        ),

        # ======================================================================
        # CLUSTER 3: CALCULUS 3 (Right Macro-Galaxy around x=520, y=20)
        # Divided into 4 clean architectural sub-rings:
        #   3A. Vector & Surface Geometry (Top-Right)
        #   3B. Multivariable Derivatives & Optimization (Lower-Right)
        #   3C. Multiple Integrals & Coordinate Jacobians (Center-Right)
        #   3D. Vector Calculus & Fundamental Theorems (Far-Right Apex)
        # ======================================================================
        # --- 3A: Vector & Surface Geometry ---
        (
            "Vectors_2D_3D",
            "2D / 3D Vectors",
            "Calculus 3",
            r"\mathbf{v} = \langle v_1, v_2, v_3 \rangle, \quad \|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2 + v_3^2}",
            [
                ("Components", r"$\mathbf{v} = v_1\mathbf{i} + v_2\mathbf{j} + v_3\mathbf{k}$"),
                ("Euclidean Norm", r"$\|\mathbf{v}\| = \sqrt{\mathbf{v} \cdot \mathbf{v}}$"),
                ("Unit Direction", r"$\hat{\mathbf{u}} = \mathbf{v} / \|\mathbf{v}\|$"),
            ],
            "Encodes magnitude and spatial direction in 2D or 3D space, serving as the fundamental language of multivariable geometry.",
            24,
            180,
            -360,
            "",
        ),
        (
            "Dot_Product",
            "Dot Product & Angle",
            "Calculus 3",
            r"\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\|\,\|\mathbf{v}\|\cos\theta = u_1v_1 + u_2v_2 + u_3v_3",
            [
                ("Algebraic Sum", r"$\sum_{i=1}^3 u_i v_i \in \mathbb{R}$ (Scalar)"),
                ("Orthogonality Test", r"$\mathbf{u} \cdot \mathbf{v} = 0 \iff \mathbf{u} \perp \mathbf{v}$"),
                ("Vector Projection", r"$\text{proj}_{\mathbf{v}}\mathbf{u} = \left(\frac{\mathbf{u}\cdot\mathbf{v}}{\|\mathbf{v}\|^2}\right)\mathbf{v}$"),
            ],
            "Compresses two vectors into a scalar measuring directional alignment, work, and orthogonal projection.",
            24,
            390,
            -420,
            "",
        ),
        (
            "Cross_Product",
            "Cross Product & Normal Vector",
            "Calculus 3",
            r"\mathbf{u} \times \mathbf{v} = \det\begin{bmatrix}\mathbf{i} & \mathbf{j} & \mathbf{k}\\ u_1 & u_2 & u_3\\ v_1 & v_2 & v_3\end{bmatrix}, \quad \|\mathbf{u}\times\mathbf{v}\| = \|\mathbf{u}\|\|\mathbf{v}\|\sin\theta",
            [
                ("Output Type", r"Vector $\mathbf{n} \perp \mathbf{u}, \mathbf{v}$ (Right-Hand Rule)"),
                ("Geometric Magnitude", r"Area of parallelogram spanned by $\mathbf{u}, \mathbf{v}$"),
                ("Parallel Test", r"$\mathbf{u} \times \mathbf{v} = \mathbf{0} \iff \mathbf{u} \parallel \mathbf{v}$"),
            ],
            "Generates a 3D vector strictly perpendicular to two input vectors whose length equals the area of their spanned parallelogram.",
            24,
            610,
            -380,
            "",
        ),
        (
            "Lines_And_Planes",
            "Equations of Lines & Planes",
            "Calculus 3",
            r"\text{Line: }\mathbf{r}(t)=\mathbf{r}_0+t\mathbf{v} \quad \big| \quad \text{Plane: }\mathbf{n}\cdot(\mathbf{r}-\mathbf{r}_0)=0",
            [
                ("3D Line", r"Point $\mathbf{r}_0$ + Direction Vector $\mathbf{v}=\langle a,b,c\rangle$"),
                ("3D Plane Scalar Form", r"$a(x-x_0) + b(y-y_0) + c(z-z_0) = 0$"),
                ("Plane Normal", r"$\mathbf{n} = \langle a, b, c \rangle \perp \text{Plane}$"),
            ],
            "Defines 3D lines by marching along a direction vector and flat planes as the set of vectors orthogonal to a normal vector.",
            22,
            510,
            -210,
            "",
        ),
        (
            "Quadric_Surfaces",
            "Quadric Surfaces",
            "Calculus 3",
            r"\pm\frac{x^2}{a^2} \pm \frac{y^2}{b^2} \pm \frac{z^2}{c^2} = 1 \quad \text{or} \quad z = \frac{x^2}{a^2} \pm \frac{y^2}{b^2}",
            [
                ("Ellipsoid / Sphere", r"$\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$ (All $+$, bounded)"),
                ("Paraboloids", r"$z = \frac{x^2}{a^2} + \frac{y^2}{b^2}$ (Bowl) or $-\frac{y^2}{b^2}$ (Saddle)"),
                ("Hyperboloids & Cone", r"1 or 2 minus signs in quadratic trace"),
            ],
            "The 3D counterparts to conic sections—ellipsoids, paraboloids, hyperboloids, and cones—classified by their 2D planar traces.",
            21,
            720,
            -210,
            "",
        ),

        # --- 3B: Multivariable Derivatives & Optimization ---
        (
            "Partial_Derivatives",
            "Partial Derivatives",
            "Calculus 3",
            r"\frac{\partial f}{\partial x} = \lim_{h \to 0} \frac{f(x+h, y) - f(x, y)}{h}",
            [
                ("Active Variable", r"Differentiate w.r.t. $x$ (or $y, z$)"),
                ("Frozen Variables", r"Hold remaining variables constant"),
                ("Clairaut's Symmetry", r"$f_{xy}(x,y) = f_{yx}(x,y)$ for smooth $f$"),
            ],
            "Slices a multivariable surface parallel to a single coordinate axis to measure the slope along that isolated direction.",
            28,
            190,
            260,
            "",
        ),
        (
            "Gradient",
            "Gradient Vector",
            "Calculus 3",
            r"\nabla f(x,y,z) = \left\langle \frac{\partial f}{\partial x},\, \frac{\partial f}{\partial y},\, \frac{\partial f}{\partial z} \right\rangle",
            [
                ("Operator Action", r"Maps scalar field $f \mapsto$ vector field $\nabla f$"),
                ("Steepest Ascent", r"Points in direction of max rate $\|\nabla f\|$"),
                ("Level Surface Normal", r"$\nabla f \perp$ level curve/surface $f(x,y,z)=k$"),
            ],
            "Packages all partial derivatives into a master compass vector pointing toward steepest ascent and perpendicular to level sets.",
            30,
            430,
            280,
            "",
        ),
        (
            "Directional_Derivative",
            "Directional Derivative",
            "Calculus 3",
            r"D_{\hat{\mathbf{u}}}f(x,y,z) = \nabla f(x,y,z) \cdot \hat{\mathbf{u}} = \|\nabla f\|\cos\theta",
            [
                ("Surface Gradient", r"$\nabla f = \langle f_x, f_y, f_z \rangle$"),
                ("Unit Direction", r"$\hat{\mathbf{u}} = \langle u_1, u_2, u_3 \rangle$ with $\|\hat{\mathbf{u}}\|=1$"),
                ("Scalar Output", r"Slope of surface when walking along $\hat{\mathbf{u}}$"),
            ],
            "Projects the gradient vector onto any unit vector u to find the instantaneous slope in an arbitrary compass direction.",
            23,
            450,
            460,
            "",
        ),
        (
            "Tangent_Plane",
            "Tangent Plane Equation",
            "Calculus 3",
            r"z - z_0 = f_x(x_0,y_0)(x - x_0) + f_y(x_0,y_0)(y - y_0)",
            [
                ("Explicit Form", r"$L(x,y) = f(x_0,y_0) + f_x\Delta x + f_y\Delta y$"),
                ("Implicit Level Form", r"$\nabla F(x_0,y_0,z_0) \cdot \langle x-x_0, y-y_0, z-z_0 \rangle = 0$"),
                ("Total Differential", r"$dz = f_x\,dx + f_y\,dy$"),
            ],
            "Constructs the best flat linear plane approximating a curved surface at a point using the gradient as its normal vector.",
            23,
            670,
            410,
            "",
        ),
        (
            "Lagrange_Multipliers",
            "Lagrange Multipliers",
            "Calculus 3",
            r"\nabla f(x,y,z) = \lambda\,\nabla g(x,y,z), \quad g(x,y,z) = k",
            [
                ("Objective Function", r"Maximize/minimize $f(x,y,z)$"),
                ("Constraint Surface", r"Subject to $g(x,y,z) = k$"),
                ("Tangency Condition", r"$\nabla f \parallel \nabla g$ (Gradients align via $\lambda$)"),
            ],
            "Finds constrained maxima and minima on a boundary surface at the exact points where objective and constraint level surfaces kiss tangentially.",
            21,
            260,
            490,
            "",
        ),

        # --- 3C: Multiple Integrals & Coordinate Transformations ---
        (
            "Double_Integral",
            "Double Integral & Area",
            "Calculus 3",
            r"\iint_{R} f(x,y)\,dA = \int_{a}^{b} \int_{g_1(x)}^{g_2(x)} f(x,y)\,dy\,dx",
            [
                ("2D Base Domain", r"Planar region $R \subset \mathbb{R}^2$, area patch $dA$"),
                ("Fubini Iteration", r"Inner integral sweeps slices; outer sums slices"),
                ("Geometric Output", r"Volume under $z=f(x,y)$ (or Area if $f=1$)"),
            ],
            "Sums infinitesimal columns over a 2D planar region R to compute signed volume under a surface, planar area, or lamina mass.",
            28,
            160,
            -40,
            "",
        ),
        (
            "Triple_Integral",
            "Triple Integral & Volume",
            "Calculus 3",
            r"\iiint_{Q} f(x,y,z)\,dV = \int_{a}^{b}\int_{h_1(x)}^{h_2(x)}\int_{g_1(x,y)}^{g_2(x,y)} f\,dz\,dy\,dx",
            [
                ("3D Solid Domain", r"Solid region $Q \subset \mathbb{R}^3$, volume box $dV$"),
                ("6 Integration Orders", r"$dz\,dy\,dx,\ dx\,dy\,dz,$ etc. by projection"),
                ("Physical Output", r"Volume ($\iiint 1\,dV$), Mass ($\iiint \rho\,dV$), Inertia"),
            ],
            "Integrates over 3D solid regions Q by stacking 1D filaments into 2D sheets and sweeping sheets across a 3D volume.",
            28,
            390,
            -30,
            "",
        ),
        (
            "Cylindrical_Spherical",
            "Cylindrical & Spherical Coords",
            "Calculus 3",
            r"dV_{\text{cyl}} = r\,dz\,dr\,d\theta \quad \big| \quad dV_{\text{sph}} = \rho^2\sin\phi\,d\rho\,d\phi\,d\theta",
            [
                ("Cylindrical Map", r"$(r\cos\theta, r\sin\theta, z) \implies J = r$"),
                ("Spherical Map", r"$(\rho\sin\phi\cos\theta, \rho\sin\phi\sin\theta, \rho\cos\phi)$"),
                ("Spherical Wedge", r"$J = \rho^2\sin\phi$ with $\phi \in [0, \pi]$"),
            ],
            "Adapts 3D integration grids to cylinders, cones, and spheres using radial and angular coordinates with built-in volume scaling factors.",
            24,
            240,
            -190,
            "",
        ),
        (
            "Jacobian",
            "Jacobian Transformation",
            "Calculus 3",
            r"\iint_{R} f(x,y)\,dx\,dy = \iint_{S} f\bigl(x(u,v),y(u,v)\bigr)\,\left|\frac{\partial(x,y)}{\partial(u,v)}\right|\,du\,dv",
            [
                ("Coordinate Map", r"$T(u,v) = \bigl(x(u,v),\, y(u,v)\bigr)$"),
                ("Jacobian Matrix Det", r"$J = \det\begin{bmatrix} x_u & x_v \\ y_u & y_v \end{bmatrix} = x_u y_v - x_v y_u$"),
                ("Area Distortion Factor", r"$dA = |J(u,v)|\,du\,dv$"),
            ],
            "The multivariable generalization of u-substitution: uses the determinant of partial derivatives to measure local area or volume distortion.",
            27,
            330,
            110,
            "",
        ),

        # --- 3D: Vector Calculus & Fundamental Theorems (Apex Cluster) ---
        (
            "Line_Integral",
            "Line Integrals (Scalar & Work)",
            "Calculus 3",
            r"\int_{C} \mathbf{F}\cdot d\mathbf{r} = \int_{a}^{b} \mathbf{F}\bigl(\mathbf{r}(t)\bigr)\cdot \mathbf{r}'(t)\,dt = \int_{C} M\,dx + N\,dy + P\,dz",
            [
                ("Parameterized Path", r"Curve $C: \mathbf{r}(t)$ for $t \in [a, b]$"),
                ("Tangent Differential", r"$d\mathbf{r} = \mathbf{r}'(t)\,dt = \mathbf{T}\,ds$"),
                ("Physical Meaning", r"Work done by force field $\mathbf{F}$ along path $C$"),
            ],
            "Integrates a scalar density or tangential vector field along a 2D or 3D space curve to compute wire mass or mechanical work.",
            26,
            610,
            140,
            "",
        ),
        (
            "FTLI",
            "Fund. Thm. of Line Integrals",
            "Calculus 3",
            r"\int_{C} \nabla f \cdot d\mathbf{r} = f\bigl(\mathbf{r}(b)\bigr) - f\bigl(\mathbf{r}(a)\bigr)",
            [
                ("Conservative Field", r"$\mathbf{F} = \nabla f$ ($\text{curl}\,\mathbf{F} = \mathbf{0}$)"),
                ("Path Independence", r"Depends only on start $\mathbf{r}(a)$ and end $\mathbf{r}(b)$"),
                ("Closed Loop Rule", r"$\oint_C \nabla f \cdot d\mathbf{r} = 0$ around any closed loop"),
            ],
            "Extends the Fundamental Theorem of Calculus to 3D space curves: work in a conservative gradient field depends solely on potential difference at the endpoints.",
            29,
            640,
            270,
            "",
        ),
        (
            "Curl_Div",
            "Curl & Divergence Operators",
            "Calculus 3",
            r"\text{curl}\,\mathbf{F} = \nabla \times \mathbf{F}, \qquad \text{div}\,\mathbf{F} = \nabla \cdot \mathbf{F} = \frac{\partial M}{\partial x}+\frac{\partial N}{\partial y}+\frac{\partial P}{\partial z}",
            [
                ("Curl (Rotation)", r"$\nabla \times \mathbf{F} = \mathbf{0} \implies \mathbf{F}$ is irrotational"),
                ("Divergence (Expansion)", r"$\nabla \cdot \mathbf{F} = 0 \implies \mathbf{F}$ is incompressible"),
                ("Vector Identity", r"$\text{div}(\text{curl}\,\mathbf{F}) = \nabla \cdot (\nabla \times \mathbf{F}) = 0$"),
            ],
            "Microscopic vector derivatives: Curl measures local paddlewheel rotation axis and speed, while Divergence measures net outward source/sink expansion.",
            26,
            790,
            20,
            "",
        ),
        (
            "Surface_Integral",
            "Surface & Flux Integrals",
            "Calculus 3",
            r"\iint_{S} \mathbf{F}\cdot \hat{\mathbf{n}}\,dS = \iint_{D} \mathbf{F}\bigl(\mathbf{r}(u,v)\bigr)\cdot (\mathbf{r}_u \times \mathbf{r}_v)\,du\,dv",
            [
                ("Surface Patch Normal", r"$\hat{\mathbf{n}}\,dS = (\mathbf{r}_u \times \mathbf{r}_v)\,du\,dv$"),
                ("Explicit Graph Form", r"For $z=g(x,y)$: $\hat{\mathbf{n}}\,dS = \langle -g_x, -g_y, 1 \rangle\,dA$"),
                ("Physical Meaning", r"Net fluid/field flux passing through surface $S$"),
            ],
            "Measures the rate of fluid or electromagnetic field flux penetrating a curved 3D surface using the cross-product normal vector.",
            26,
            660,
            -60,
            "",
        ),
        (
            "Greens_Theorem",
            "Green's Theorem (2D)",
            "Calculus 3",
            r"\oint_{\partial R} (M\,dx + N\,dy) = \iint_{R} \left(\frac{\partial N}{\partial x} - \frac{\partial M}{\partial y}\right) dA",
            [
                ("1D Boundary Loop", r"Positively oriented (CCW) curve $C = \partial R$"),
                ("2D Interior Curl", r"$(\nabla \times \mathbf{F})\cdot\mathbf{k} = N_x - M_y$"),
                ("Normal Flux Form", r"$\oint_C \mathbf{F}\cdot\mathbf{n}\,ds = \iint_R (\nabla\cdot\mathbf{F})\,dA$"),
            ],
            "Equates macroscopic circulation around a closed 2D boundary curve to the double integral of microscopic curl across the enclosed region.",
            33,
            880,
            190,
            "13.451476",
        ),
        (
            "Stokes_Theorem",
            "Stokes' Theorem (3D Surface)",
            "Calculus 3",
            r"\oint_{\partial S} \mathbf{F} \cdot d\mathbf{r} = \iint_{S} (\nabla \times \mathbf{F}) \cdot \hat{\mathbf{n}}\,dS",
            [
                ("1D Boundary Rim", r"Closed 3D space curve $C = \partial S$ (Right-Hand Rule)"),
                ("2D Capping Surface", r"Oriented smooth surface $S$ in $\mathbb{R}^3$"),
                ("Unifying Operator", r"Boundary circulation = Surface flux of Curl"),
            ],
            "Lifts Green's Theorem into 3D space: the line integral around the rim of a 3D surface equals the total flux of curl piercing the surface.",
            32,
            1060,
            70,
            "19.820410",
        ),
        (
            "Divergence_Theorem",
            "Divergence Theorem (Gauss)",
            "Calculus 3",
            r"\iint_{\partial Q} \mathbf{F} \cdot \hat{\mathbf{n}}\,dS = \iiint_{Q} (\nabla \cdot \mathbf{F})\,dV",
            [
                ("2D Closed Shell", r"Outward-oriented boundary surface $S = \partial Q$"),
                ("3D Solid Interior", r"Enclosed solid volume $Q \subset \mathbb{R}^3$"),
                ("Unifying Operator", r"Boundary outward flux = Volume sum of Divergence"),
            ],
            "The 3D culmination of the Fundamental Theorem: total outward flux escaping a closed surface equals the triple integral of sources and sinks inside.",
            32,
            1040,
            -120,
            "24.109385",
        ),
    ]

    for (
        node_id,
        label,
        group,
        latex_formula,
        arch,
        desc,
        size,
        x_pos,
        y_pos,
        hub_badge,
    ) in nodes_data:
        tooltip_html = make_tooltip(
            node_id, label, group, latex_formula, arch, desc, hub_badge
        )
        G.add_node(
            node_id,
            label=label,
            group=group,
            color=COURSE_COLORS[group],
            title=tooltip_html,
            size=size,
            x=x_pos,
            y=y_pos,
        )
        node_metadata[node_id] = {
            "id": node_id,
            "label": label,
            "group": group,
            "color": COURSE_COLORS[group],
            "latex": latex_formula,
            "architecture": arch,
            "description": desc,
            "badge": hub_badge,
            "size": size,
            "x": x_pos,
            "y": y_pos,
        }

    # --------------------------------------------------------------------------
    # Directed Edges (Core Threads + Intra-Cluster Structural Web)
    # --------------------------------------------------------------------------
    edges_data = [
        # === Thread 1: Fundamental Theorem Chain ===
        ("FTC", "FTLI", "Generalizes 1D [a,b] to 3D Space Curves"),
        ("FTLI", "Greens_Theorem", "1D Curve Endpoints to 2D Closed Boundary"),
        ("Greens_Theorem", "Stokes_Theorem", "2D Planar Region to 3D Curved Surface"),
        ("Greens_Theorem", "Divergence_Theorem", "2D Flux Form to 3D Closed Solid"),

        # === Thread 2: Derivative & Rate of Change Chain ===
        ("Limits_Continuity", "Single_Derivative", "Difference Quotient Limit h→0"),
        ("Single_Derivative", "Chain_Rule", "Composite Rate Multiplication"),
        ("Single_Derivative", "Optimization_1D", "Stationary Points f'(c) = 0"),
        ("Single_Derivative", "Partial_Derivatives", "Axis-Aligned Multivariable Slice"),
        ("Partial_Derivatives", "Gradient", "Assembles Vector ∇f = ⟨fx, fy, fz⟩"),
        ("Gradient", "Directional_Derivative", "Dot Product D_u f = ∇f · u"),
        ("Directional_Derivative", "Tangent_Plane", "Zero-Slope Level Set Orthogonal to ∇F"),
        ("Gradient", "Tangent_Plane", "Defines Surface Normal Vector"),
        ("Gradient", "Lagrange_Multipliers", "Parallel Gradients ∇f = λ∇g"),
        ("Optimization_1D", "Lagrange_Multipliers", "Constrained Multivariable Extrema"),
        ("Single_Derivative", "Taylor_Series", "n-th Order Derivative Coefficients"),

        # === Thread 3: Integration & Coordinate Transformation Chain ===
        ("Limits_Continuity", "Definite_Integral", "Infinite Limit of Riemann Sums"),
        ("Definite_Integral", "FTC", "Links Area Accumulation to Antiderivative"),
        ("Single_Derivative", "FTC", "Inverse Differentiation-Integration Pair"),
        ("Chain_Rule", "U_Substitution", "Reverses Composite Derivative"),
        ("Definite_Integral", "U_Substitution", "1D Differential Scaling du = g'(x)dx"),
        ("Definite_Integral", "Integration_By_Parts", "Reverses Product Rule"),
        ("U_Substitution", "Trig_Sub", "Trigonometric Identity Substitution"),
        ("Integration_By_Parts", "Partial_Fractions", "Rational Antiderivative Techniques"),
        ("Trig_Sub", "Polar_Coordinates", "Maps x=r cosθ, y=r sinθ"),
        ("Polar_Coordinates", "Double_Integral", "Polar Area Element dA = r dr dθ"),
        ("Definite_Integral", "Double_Integral", "Iterates 1D Slice over 2D Region"),
        ("Integration_By_Parts", "Double_Integral", "Evaluates Iterated Primitives"),
        ("Double_Integral", "Triple_Integral", "Stacks 2D Regions into 3D Solid Volume"),
        ("Polar_Coordinates", "Cylindrical_Spherical", "Lifts 2D Polar into 3D Space"),
        ("Triple_Integral", "Cylindrical_Spherical", "Transforms dV into r and ρ²sinφ"),
        ("Cylindrical_Spherical", "Jacobian", "Special Cases of 3D Jacobian Determinant"),
        ("U_Substitution", "Jacobian", "Generalizes du/dx to |∂(x,y)/∂(u,v)|"),
        ("Partial_Derivatives", "Jacobian", "Matrix of First Partial Derivatives"),
        ("Jacobian", "Double_Integral", "Scales Planar Area dA = |J| du dv"),
        ("Jacobian", "Triple_Integral", "Scales Volume dV = |J| du dv dw"),

        # === Thread 4: Vectors & Multivariable Geometry Chain ===
        ("Parametric_Curves", "Vectors_2D_3D", "Position & Velocity Vector r(t)"),
        ("Vectors_2D_3D", "Dot_Product", "Scalar Projection & Angle cosθ"),
        ("Vectors_2D_3D", "Cross_Product", "3D Orthogonal Area Vector"),
        ("Dot_Product", "Cross_Product", "Orthogonal Complement Identities"),
        ("Cross_Product", "Lines_And_Planes", "Generates Normal Vector n = u × v"),
        ("Dot_Product", "Lines_And_Planes", "Normal Plane Eq: n · (r - r₀) = 0"),
        ("Lines_And_Planes", "Quadric_Surfaces", "Extends Linear Planes to 2nd-Degree Surfaces"),
        ("Quadric_Surfaces", "Triple_Integral", "Defines 3D Bounding Surfaces"),
        ("Lines_And_Planes", "Tangent_Plane", "Point-Normal Plane Representation"),

        # === Cross-Thread Bridges & Constellation Web Links ===
        ("Dot_Product", "Directional_Derivative", "Projects ∇f onto Unit Direction u"),
        ("Parametric_Curves", "Line_Integral", "Parameterizes Curve C: r(t)"),
        ("Dot_Product", "Line_Integral", "Integrates Tangential Work F · dr"),
        ("Line_Integral", "FTLI", "Evaluates Conservative Field F = ∇f"),
        ("Gradient", "FTLI", "Provides Potential Function ∇f"),
        ("Partial_Derivatives", "Curl_Div", "Applies Del Operator ∇ to Vector Fields"),
        ("Cross_Product", "Curl_Div", "Curl = ∇ × F"),
        ("Dot_Product", "Curl_Div", "Divergence = ∇ · F"),
        ("Cross_Product", "Surface_Integral", "Oriented Patch dS = (r_u × r_v) du dv"),
        ("Double_Integral", "Greens_Theorem", "Evaluates ∬_R (Nx - My) dA"),
        ("Double_Integral", "Surface_Integral", "Integrates over Parameter Domain D"),
        ("Surface_Integral", "Stokes_Theorem", "Evaluates Surface Flux of Curl"),
        ("Curl_Div", "Stokes_Theorem", "Integrand (∇ × F) · n"),
        ("Line_Integral", "Stokes_Theorem", "Boundary Circulation ∮_∂S F · dr"),
        ("Surface_Integral", "Divergence_Theorem", "Closed Boundary Flux ∬_∂Q F · n dS"),
        ("Triple_Integral", "Divergence_Theorem", "Evaluates Interior ∭_Q (∇ · F) dV"),
        ("Curl_Div", "Divergence_Theorem", "Integrand div(F) = ∇ · F"),
    ]

    for src, dst, rel_label in edges_data:
        is_cross_cluster = G.nodes[src]["group"] != G.nodes[dst]["group"]
        G.add_edge(
            src,
            dst,
            label="",  # Hidden by default for clean constellation look; shown dynamically on focus
            rel_text=rel_label,
            title=f"{src.replace('_', ' ')} → {dst.replace('_', ' ')}: {rel_label}",
            width=1.6 if is_cross_cluster else 1.2,
            arrows={"to": {"enabled": True, "scaleFactor": 0.55}},
            color={
                "color": "rgba(91, 105, 127, 0.20)"
                if is_cross_cluster
                else "rgba(91, 105, 127, 0.28)",
                "highlight": "#D9959E",
                "hover": "#7A879A",
            },
            smooth={
                "enabled": True,
                "type": "curvedCW" if is_cross_cluster else "continuous",
                "roundness": 0.22 if is_cross_cluster else 0.12,
            },
        )

    return G, node_metadata


# ==============================================================================
# 3. Pyvis Network Configuration & Custom Constellation UI Export
# ==============================================================================
def create_interactive_network(
    G: nx.DiGraph,
    node_metadata: dict,
    output_filename: str = "calculus_network.html",
) -> None:
    """
    Exports the NetworkX graph to an interactive Pyvis HTML file with:
    - Obsidian constellation styling & glowing nodes
    - Floating crimson hub callouts (matching reference aesthetic)
    - KaTeX mathematical formula rendering
    - Interactive Inspector Drawer & Step-by-Step Thread Follower
    """
    # Required Pyvis setup parameters
    net = Network(
        height="800px",
        width="100%",
        bgcolor="#F7F8FB",
        font_color="#384455",
        directed=True,
        cdn_resources="remote",
    )

    net.from_nx(G)

    # Style nodes for crisp readability and generous spacing
    for node in net.nodes:
        nid = node["id"]
        meta = node_metadata[nid]
        node["shape"] = "dot"
        node["borderWidth"] = 2
        node["borderWidthSelected"] = 4
        node["shadow"] = {
            "enabled": True,
            "color": meta["color"],
            "size": 18,
            "x": 0,
            "y": 0,
        }
        node["font"] = {
            "size": 13,
            "color": "#384455",
            "face": "Inter, Segoe UI, sans-serif",
            "strokeWidth": 3,
            "strokeColor": "#F7F8FB",
        }

    # Enable required Pyvis control buttons
    net.show_buttons(filter_=["physics", "nodes", "edges"])

    net.write_html(output_filename)

    # Serialize metadata and threads for client-side interactive architecture
    meta_json = json.dumps(node_metadata)
    threads_json = json.dumps(THREADS)
    worked_examples_json = json.dumps(WORKED_EXAMPLES)

    custom_enhancement = f"""
    <!-- KaTeX for textbook-grade mathematical formula rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>

    <style>
      * {{ box-sizing: border-box; }}
      :root {{
        --ink: #384455;
        --muted: #687589;
        --line: #d9deea;
        --accent: #c9828e;
        --accent-soft: #f5e4e6;
        --surface: rgba(255, 255, 255, 0.94);
      }}
      html, body {{
        margin: 0 !important;
        padding: 0 !important;
        background: linear-gradient(135deg, #fcfaf5 0%, #f3f7fb 54%, #fff4f4 100%) !important;
        color: var(--ink);
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        overflow-x: hidden;
      }}
      .card {{
        background-color: transparent !important;
        border: none !important;
      }}
      #mynetwork {{
        height: 100vh !important;
        width: 100vw !important;
        background: linear-gradient(135deg, #fcfaf5 0%, #f3f7fb 54%, #fff4f4 100%) !important;
        border: none !important;
      }}

      /* Top-Left Constellation Control HUD */
      #calc-hud {{
        position: fixed;
        top: 16px;
        left: 16px;
        z-index: 9000;
        width: 350px;
        background: var(--surface);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(86, 100, 122, 0.18);
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 12px 32px rgba(72, 82, 102, 0.14);
      }}
      .hud-title {{
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--ink);
        margin: 0 0 4px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
      }}
      .hud-subtitle {{
        font-size: 11px;
        color: var(--muted);
        margin-bottom: 12px;
      }}
      .hud-section-label {{
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.9px;
        color: #8993a2;
        margin: 10px 0 6px 0;
      }}
      .btn-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
      }}
      .hud-btn {{
        cursor: pointer;
        background: #f4f6fa;
        border: 1px solid #dce1eb;
        color: #4b586d;
        border-radius: 5px;
        padding: 5px 9px;
        font-size: 11px;
        font-weight: 600;
        transition: all 0.18s ease;
      }}
      .hud-btn:hover {{
        background: #eaf0f6;
        border-color: #bdc8d8;
      }}
      .hud-btn.active {{
        background: #f1dadd;
        border-color: #d7a4aa;
        color: #704b54;
        box-shadow: 0 2px 8px rgba(174, 116, 128, 0.14);
      }}
      .thread-btn {{
        width: 100%;
        text-align: left;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 10px;
      }}

      /* Guided Step-by-Step Bar */
      #stepper-panel {{
        display: none;
        margin-top: 10px;
        padding: 10px;
        background: #fbf1f1;
        border: 1px solid #e8cdd0;
        border-radius: 6px;
      }}
      .stepper-controls {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 6px;
        margin-top: 6px;
      }}

      /* Right-Side Architectural Formula Inspector */
      #formula-inspector {{
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 9000;
        width: 410px;
        max-height: calc(100vh - 32px);
        overflow-y: auto;
        background: var(--surface);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(86, 100, 122, 0.18);
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 16px 40px rgba(72, 82, 102, 0.16);
      }}
      .insp-badge {{
        display: inline-block;
        background: #f1dadd;
        color: #704b54;
        font-family: 'Consolas', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 3px;
      }}
      .insp-formula-box {{
        margin: 12px 0;
        padding: 14px 12px;
        background: #f7f8fb;
        border: 1px solid #e0e5ee;
        border-radius: 6px;
        color: #65738a;
        font-size: 15px;
        text-align: center;
        overflow-x: auto;
      }}
      .arch-grid {{
        display: flex;
        flex-direction: column;
        gap: 6px;
        margin: 10px 0;
        background: #f5f7fa;
        padding: 10px 12px;
        border-radius: 6px;
        border: 1px solid #e2e6ee;
      }}
      .arch-item {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        font-size: 12px;
        padding-bottom: 5px;
        border-bottom: 1px solid #e2e6ee;
      }}
      .arch-item:last-child {{ border-bottom: none; padding-bottom: 0; }}
      .flow-pill {{
        cursor: pointer;
        display: inline-block;
        margin: 3px 4px 3px 0;
        padding: 4px 8px;
        font-size: 11px;
        background: #f3f5f9;
        border: 1px solid #dce1eb;
        border-radius: 4px;
        color: #4b586d;
        transition: background 0.15s;
      }}
      .flow-pill:hover {{
        background: #f1dadd;
        border-color: #d7a4aa;
      }}
      .prereq-tree {{
        list-style: none;
        margin: 4px 0 0;
        padding-left: 13px;
        border-left: 1px solid #d8deea;
      }}
      .prereq-tree > li {{
        position: relative;
        margin: 5px 0;
        padding-left: 8px;
      }}
      .prereq-tree > li::before {{
        content: '';
        position: absolute;
        top: 12px;
        left: -13px;
        width: 12px;
        border-top: 1px solid #d8deea;
      }}
      .prereq-link {{
        max-width: 100%;
        cursor: pointer;
        background: #f3f5f9;
        border: 1px solid #dce1eb;
        border-radius: 4px;
        color: #46546a;
        padding: 4px 7px;
        text-align: left;
        font: inherit;
        font-size: 11px;
      }}
      .prereq-link:hover {{
        background: #f1dadd;
        border-color: #d7a4aa;
      }}
      .prereq-relation {{
        display: block;
        max-width: 34ch;
        margin: 3px 4px 5px;
        color: #788497;
        font-size: 10px;
        line-height: 1.4;
      }}
      .worked-example {{
        margin-top: 16px;
        padding-top: 14px;
        border-top: 1px solid #e0e5ee;
      }}
      .worked-example-title {{
        margin: 0 0 8px;
        color: #bd7884;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
      }}
      .example-problem {{
        padding: 9px 10px;
        border: 1px solid #e2e6ee;
        border-radius: 6px;
        background: #f5f7fa;
        color: #526074;
        font-size: 12px;
        line-height: 1.5;
      }}
      .example-step-heading {{
        margin: 12px 0 4px;
        color: #384455;
        font-size: 13px;
      }}
      .example-step-copy {{
        margin: 4px 0 8px;
        color: #526074;
        font-size: 12px;
        line-height: 1.5;
      }}
      .example-math {{
        overflow-x: auto;
        padding: 9px 8px;
        border: 1px solid #e2e6ee;
        border-radius: 6px;
        background: #f7f8fb;
        color: #384455;
        text-align: center;
      }}
      .example-prerequisites {{
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-top: 9px;
      }}
      .example-prerequisite {{
        cursor: pointer;
        padding: 4px 7px;
        border: 1px solid #dce1eb;
        border-radius: 4px;
        background: #f3f5f9;
        color: #526074;
        font-size: 10px;
      }}
      .example-prerequisite:hover {{
        background: #f1dadd;
        border-color: #d7a4aa;
      }}
      .example-step-controls {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        margin-top: 10px;
      }}
      #insp-desc, #stepper-progress {{ color: #526074 !important; }}
      #insp-title {{ color: var(--ink) !important; }}
      #formula-inspector [style*="color:#ff2a4b"],
      #calc-hud [style*="color:#ff2a4b"] {{ color: var(--accent) !important; }}
      #formula-inspector [style*="color:#ffffff"],
      #formula-inspector [style*="color:#fff"],
      #calc-hud [style*="color:#ffffff"],
      #calc-hud [style*="color:#fff"] {{ color: var(--ink) !important; }}
      #formula-inspector [style*="color:#9ca3af"] {{ color: var(--muted) !important; }}
      #formula-inspector > div:last-child {{ border-color: #e0e5ee !important; }}
      .arch-item span {{ color: #536176 !important; }}
      .arch-item .katex-inline {{ color: var(--ink) !important; }}
      .calc-tooltip-card {{ color: var(--ink) !important; }}
      .calc-tooltip-card [style*="color:#ffffff"],
      .calc-tooltip-card [style*="color:#f3f4f6"] {{ color: var(--ink) !important; }}
      .calc-tooltip-card [style*="rgba(255,255,255,0.07)"] {{ border-color: #e2e6ee !important; }}
      .calc-tooltip-card .katex-inline {{ color: var(--ink) !important; }}

      @media (max-width: 760px) {{
        #calc-hud {{ width: min(350px, calc(100vw - 24px)); max-height: 42vh; overflow-y: auto; top: 12px; left: 12px; }}
        #formula-inspector {{ top: auto; right: 12px; bottom: 12px; width: min(410px, calc(100vw - 24px)); max-height: 48vh; }}
        #config {{ width: min(420px, calc(100vw - 24px)); }}
      }}

      /* Collapsible Pyvis Native Physics Config */
      #config {{
        display: none;
        position: fixed;
        bottom: 16px;
        left: 16px;
        z-index: 9500;
        max-height: 45vh;
        width: 420px;
        overflow-y: auto;
        background: rgba(255, 255, 255, 0.98) !important;
        border: 1px solid #d9deea !important;
        border-radius: 8px;
        padding: 12px;
        color: #384455 !important;
      }}
      div.vis-tooltip {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
      }}
    </style>

    <!-- Left Control HUD -->
    <div id="calc-hud">
      <div class="hud-title">
        <span>Calculus Constellation</span>
        <span style="font-size:10px; color:#c9828e; font-family:monospace;">34 NODES • 61 LINKS</span>
      </div>
      <div class="hud-subtitle">Click any node or step through a thread to inspect its architecture.</div>

      <div class="hud-section-label">1. Visual Aesthetic Mode</div>
      <div class="btn-row">
        <button id="theme-constellation" class="hud-btn" onclick="setVisualTheme('constellation')">
          Soft Constellation
        </button>
        <button id="theme-course" class="hud-btn active" onclick="setVisualTheme('course')">
          Pastel Course Colors
        </button>
      </div>

      <div class="hud-section-label">2. Filter by Course Galaxy</div>
      <div class="btn-row">
        <button id="flt-ALL" class="hud-btn active" onclick="filterCourse('ALL')">All Galaxies</button>
        <button id="flt-Calculus 1" class="hud-btn" style="border-left:3px solid #AFC9E8;" onclick="filterCourse('Calculus 1')">Calc 1</button>
        <button id="flt-Calculus 2" class="hud-btn" style="border-left:3px solid #B9D7C2;" onclick="filterCourse('Calculus 2')">Calc 2</button>
        <button id="flt-Calculus 3" class="hud-btn" style="border-left:3px solid #E7B8C8;" onclick="filterCourse('Calculus 3')">Calc 3</button>
      </div>

      <div class="hud-section-label">3. Guided Follow-Through Threads</div>
      <div class="btn-row" style="flex-direction:column;">
        <button id="th-thread_1" class="hud-btn thread-btn" onclick="activateThread('thread_1')">
          <span>Thread 1: Fundamental Theorems</span><span>5 steps →</span>
        </button>
        <button id="th-thread_2" class="hud-btn thread-btn" onclick="activateThread('thread_2')">
          <span>Thread 2: Derivatives & Gradients</span><span>7 steps →</span>
        </button>
        <button id="th-thread_3" class="hud-btn thread-btn" onclick="activateThread('thread_3')">
          <span>Thread 3: Integrals & Jacobians</span><span>9 steps →</span>
        </button>
        <button id="th-thread_4" class="hud-btn thread-btn" onclick="activateThread('thread_4')">
          <span>Thread 4: Vectors & 3D Surfaces</span><span>6 steps →</span>
        </button>
      </div>

      <div id="stepper-panel">
        <div id="stepper-title" style="font-size:11px; font-weight:700; color:#c9828e;"></div>
        <div id="stepper-progress" style="font-size:12px; color:#384455; margin-top:2px;"></div>
        <div class="stepper-controls">
          <button class="hud-btn" onclick="stepThread(-1)">← Prev</button>
          <button class="hud-btn" onclick="resetHighlight()">Overview</button>
          <button class="hud-btn active" onclick="stepThread(1)">Next Step →</button>
        </div>
      </div>

      <div class="hud-section-label">4. Layout & Physics Controls</div>
      <div class="btn-row">
        <button class="hud-btn" onclick="network.fit({{animation:{{duration:700, easingFunction:'easeInOutQuad'}}}})">Fit Canvas</button>
        <button id="btn-freeze" class="hud-btn" onclick="togglePhysicsFreeze()">Freeze Layout</button>
        <button class="hud-btn" onclick="togglePyvisConfig()">Engine Sliders</button>
      </div>
    </div>

    <!-- Right Formula Architecture Inspector -->
    <div id="formula-inspector">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span id="insp-course" style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#FF70A6;">
          CALCULUS 3
        </span>
        <span id="insp-badge" class="insp-badge">13.451476</span>
      </div>
      <h3 id="insp-title" style="margin:6px 0 4px 0; font-size:18px; color:#384455;">Green's Theorem (2D)</h3>
      <div id="insp-formula" class="insp-formula-box"></div>

      <div style="font-size:10.5px; text-transform:uppercase; letter-spacing:0.9px; color:#c9828e; font-weight:700; margin-top:10px;">
        Formula Architecture & Symbol Roles
      </div>
      <div id="insp-arch" class="arch-grid"></div>

      <div style="font-size:10.5px; text-transform:uppercase; letter-spacing:0.9px; color:#9ca3af; font-weight:700; margin-top:12px;">
        Conceptual Mechanism
      </div>
      <p id="insp-desc" style="font-size:12.5px; line-height:1.55; color:#526074; margin:6px 0 12px 0;"></p>

      <div style="border-top:1px solid #e0e5ee; padding-top:10px;">
        <div style="font-size:10.5px; text-transform:uppercase; letter-spacing:0.8px; color:#9ca3af; font-weight:700; margin-bottom:4px;">
          ← Prerequisite Foundations
        </div>
        <div id="insp-prereqs"></div>

        <div style="font-size:10.5px; text-transform:uppercase; letter-spacing:0.8px; color:#9ca3af; font-weight:700; margin:10px 0 4px 0;">
          Generalizes / Flows Into →
        </div>
        <div id="insp-next"></div>
      </div>

      <section id="worked-example" class="worked-example" style="display:none;">
        <h4 class="worked-example-title">Worked Example</h4>
        <div id="example-problem" class="example-problem"></div>
        <div id="example-step-number" style="margin-top:10px; color:#8993a2; font-size:10px;"></div>
        <h5 id="example-step-heading" class="example-step-heading"></h5>
        <p id="example-step-copy" class="example-step-copy"></p>
        <div id="example-math" class="example-math"></div>
        <div id="example-prerequisites" class="example-prerequisites"></div>
        <div class="example-step-controls">
          <button class="hud-btn" onclick="stepWorkedExample(-1)">Previous</button>
          <button class="hud-btn active" onclick="stepWorkedExample(1)">Next Step</button>
        </div>
      </section>
    </div>

    <script>
      const NODE_META = {meta_json};
      const THREADS = {threads_json};
      const WORKED_EXAMPLES = {worked_examples_json};
      let currentTheme = 'course';
      let activeThreadKey = null;
      let activeStepIdx = 0;
      let activeExampleNodeId = null;
      let activeExampleStepIdx = 0;
      let physicsFrozen = false;

      // Render KaTeX inside a DOM element
      function typesetMathInElement(el) {{
        if (typeof katex === 'undefined' || !el) return;
        const displayBoxes = el.querySelectorAll('.katex-display-box');
        displayBoxes.forEach(box => {{
          const rawLatex = box.getAttribute('data-latex');
          if (rawLatex) {{
            try {{
              katex.render(rawLatex, box, {{ displayMode: true, throwOnError: false }});
            }} catch (e) {{}}
          }}
        }});
        const inlineSpans = el.querySelectorAll('.katex-inline');
        inlineSpans.forEach(sp => {{
          const text = sp.innerHTML;
          if (text.includes('$')) {{
            sp.innerHTML = text.replace(/\\$([^$]+)\\$/g, function(_, math) {{
              try {{
                return katex.renderToString(math, {{ displayMode: false, throwOnError: false }});
              }} catch (e) {{ return math; }}
            }});
          }}
        }});
      }}

      // Configure spread-out ForceAtlas2 constellation physics & custom canvas badges
      function initConstellationGraph() {{
        if (typeof network === 'undefined' || typeof nodes === 'undefined') return;

        // Convert HTML tooltip strings into DOM elements with KaTeX rendered formulas
        nodes.forEach(function(n) {{
          if (typeof n.title === 'string' && n.title.trim().startsWith('<div')) {{
            const wrapper = document.createElement('div');
            wrapper.innerHTML = n.title;
            typesetMathInElement(wrapper);
            nodes.update({{ id: n.id, title: wrapper }});
          }}
        }});

        // Apply generous repulsion so nodes spread out cleanly in 3 distinct clusters
        network.setOptions({{
          physics: {{
            enabled: true,
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {{
              gravitationalConstant: -165,
              centralGravity: 0.0035,
              springLength: 230,
              springConstant: 0.025,
              damping: 0.65,
              avoidOverlap: 0.85
            }},
            stabilization: {{
              enabled: true,
              iterations: 180,
              updateInterval: 25
            }}
          }},
          interaction: {{
            hover: true,
            tooltipDelay: 80,
            hideEdgesOnDrag: false,
            navigationButtons: false
          }}
        }});

        // Start with the course-specific pastel node colors.
        setVisualTheme('course');

        // Draw floating crimson callout tags on key cluster hubs (matching reference image)
        network.on('afterDrawing', function(ctx) {{
          const positions = network.getPositions();
          Object.keys(NODE_META).forEach(function(nid) {{
            const meta = NODE_META[nid];
            const nodeObj = nodes.get(nid);
            if (!meta.badge || !positions[nid] || (nodeObj && nodeObj.hidden)) return;

            const pos = positions[nid];
            const text = meta.badge;
            ctx.save();
            ctx.font = 'bold 11px Consolas, monospace';
            const textWidth = ctx.measureText(text).width;
            const padX = 6;
            const boxW = textWidth + padX * 2;
            const boxH = 18;
            const boxX = pos.x + 12;
            const boxY = pos.y - 22;

            // Muted pastel callout for key nodes.
            ctx.fillStyle = '#d9959e';
            ctx.shadowColor = 'rgba(217, 149, 158, 0.28)';
            ctx.shadowBlur = 6;
            ctx.beginPath();
            ctx.roundRect(boxX, boxY, boxW, boxH, 2);
            ctx.fill();

            // Crisp white metric text
            ctx.shadowBlur = 0;
            ctx.fillStyle = '#384455';
            ctx.textBaseline = 'middle';
            ctx.fillText(text, boxX + padX, boxY + boxH / 2);
            ctx.restore();
          }});
        }});

        // Click node to inspect formula architecture & highlight direct connections
        network.on('click', function(params) {{
          if (params.nodes && params.nodes.length > 0) {{
            const clickedId = params.nodes[0];
            inspectNode(clickedId);
            if (WORKED_EXAMPLES[clickedId]) {{
              highlightWorkedExampleStep();
            }} else {{
              highlightNodeNeighborhood(clickedId);
            }}
          }} else {{
            resetHighlight();
          }}
        }});

        // Initialize inspector with Green's Theorem
        inspectNode('Greens_Theorem');
        highlightWorkedExampleStep();
      }}

      // Populate Right-Side Inspector Panel with LaTeX & Architectural Breakdown
      function inspectNode(nodeId) {{
        const meta = NODE_META[nodeId];
        if (!meta) return;

        const courseEl = document.getElementById('insp-course');
        courseEl.textContent = meta.group;
        courseEl.style.color = meta.color;

        const badgeEl = document.getElementById('insp-badge');
        if (meta.badge) {{
          badgeEl.style.display = 'inline-block';
          badgeEl.textContent = meta.badge;
        }} else {{
          badgeEl.style.display = 'none';
        }}

        document.getElementById('insp-title').textContent = meta.label;
        document.getElementById('insp-desc').textContent = meta.description;

        const formulaBox = document.getElementById('insp-formula');
        if (typeof katex !== 'undefined') {{
          katex.render(meta.latex, formulaBox, {{ displayMode: true, throwOnError: false }});
        }} else {{
          formulaBox.textContent = meta.latex;
        }}

        const archContainer = document.getElementById('insp-arch');
        archContainer.innerHTML = meta.architecture.map(item => `
          <div class="arch-item">
            <span style="color:#687589; font-weight:600;">${{item[0]}}</span>
            <span class="katex-inline" style="color:#384455; text-align:right;">${{item[1]}}</span>
          </div>
        `).join('');
        typesetMathInElement(archContainer);
        renderWorkedExampleForNode(nodeId);

        // Gather direct relations and expand upstream prerequisites into a tree.
        const allEdges = edges.get();
        const nexts = allEdges.filter(e => e.from === nodeId).map(e => e.to);

        const prereqDiv = document.getElementById('insp-prereqs');
        const prereqTreeItems = renderPrerequisiteTreeItems(nodeId, new Set([nodeId]), allEdges);
        prereqDiv.innerHTML = prereqTreeItems
          ? `<ul class="prereq-tree">${{prereqTreeItems}}</ul>`
          : '<span style="font-size:11px; color:#6b7280;">Foundational Root Concept</span>';

        const nextDiv = document.getElementById('insp-next');
        nextDiv.innerHTML = nexts.length
          ? nexts.map(nid => `<span class="flow-pill" onclick="focusAndInspect('${{nid}}')">${{NODE_META[nid].label}}</span>`).join('')
          : '<span style="font-size:11px; color:#6b7280;">Apex Theorem</span>';
      }}

      function renderWorkedExampleForNode(nodeId) {{
        const panel = document.getElementById('worked-example');
        const example = WORKED_EXAMPLES[nodeId];
        if (!example) {{
          panel.style.display = 'none';
          activeExampleNodeId = null;
          activeExampleStepIdx = 0;
          return;
        }}

        if (activeExampleNodeId !== nodeId) {{
          activeExampleNodeId = nodeId;
          activeExampleStepIdx = 0;
        }}
        panel.style.display = 'block';
        const problem = document.getElementById('example-problem');
        problem.innerHTML = `<span class="katex-inline">${{example.problem}}</span>`;
        typesetMathInElement(problem);
        renderWorkedExampleStep();
      }}

      function renderWorkedExampleStep() {{
        const example = WORKED_EXAMPLES[activeExampleNodeId];
        if (!example) return;
        const step = example.steps[activeExampleStepIdx];
        document.getElementById('example-step-number').textContent =
          `Step ${{activeExampleStepIdx + 1}} of ${{example.steps.length}}`;
        document.getElementById('example-step-heading').textContent = step.title;
        document.getElementById('example-step-copy').textContent = step.explanation;

        const equation = document.getElementById('example-math');
        if (typeof katex !== 'undefined') {{
          katex.render(step.latex, equation, {{ displayMode: true, throwOnError: false }});
        }} else {{
          equation.textContent = step.latex;
        }}

        document.getElementById('example-prerequisites').innerHTML =
          step.prerequisites.map(prerequisiteId =>
            `<button class="example-prerequisite" onclick="focusExamplePrerequisite('${{prerequisiteId}}')">${{NODE_META[prerequisiteId].label}}</button>`
          ).join('');
      }}

      function highlightWorkedExampleStep() {{
        const example = WORKED_EXAMPLES[activeExampleNodeId];
        if (!example) return;
        const step = example.steps[activeExampleStepIdx];
        const highlightedIds = new Set([step.focus, ...step.prerequisites]);

        nodes.update(nodes.get().map(node => ({{
          id: node.id,
          opacity: highlightedIds.has(node.id) ? 1.0 : 0.24,
          font: {{ color: highlightedIds.has(node.id) ? '#384455' : '#8994a5', size: 13 }}
        }})));

        edges.update(edges.get().map(edge => {{
          const isRelevant = highlightedIds.has(edge.from) && highlightedIds.has(edge.to);
          return {{
            id: edge.id,
            label: isRelevant ? (edge.rel_text || '') : '',
            width: isRelevant ? 2.8 : 0.8,
            color: {{ color: isRelevant ? '#c9828e' : 'rgba(91, 105, 127, 0.08)' }},
            font: {{ size: 11, color: '#526074', background: 'rgba(255,255,255,0.90)', strokeWidth: 0 }}
          }};
        }}));

        network.selectNodes([step.focus]);
        network.focus(step.focus, {{
          scale: 1.08,
          animation: {{ duration: 500, easingFunction: 'easeInOutQuad' }}
        }});
      }}

      function focusExamplePrerequisite(nodeId) {{
        network.selectNodes([nodeId]);
        network.focus(nodeId, {{
          scale: 1.12,
          animation: {{ duration: 500, easingFunction: 'easeInOutQuad' }}
        }});
      }}

      function stepWorkedExample(delta) {{
        const example = WORKED_EXAMPLES[activeExampleNodeId];
        if (!example) return;
        activeExampleStepIdx = (activeExampleStepIdx + delta + example.steps.length) % example.steps.length;
        renderWorkedExampleStep();
        highlightWorkedExampleStep();
      }}

      function renderPrerequisiteTreeItems(nodeId, branch, allEdges) {{
        const directPrerequisites = allEdges.filter(edge => edge.to === nodeId);
        return directPrerequisites.map(edge => {{
          const prerequisiteId = edge.from;
          const label = NODE_META[prerequisiteId].label;
          const link = `<button class="prereq-link" onclick="focusAndInspect('${{prerequisiteId}}')">${{label}}</button>`;
          const relation = edge.rel_text
            ? `<span class="prereq-relation">${{edge.rel_text}}</span>`
            : '';
          if (branch.has(prerequisiteId)) return `<li>${{link}}${{relation}}</li>`;

          branch.add(prerequisiteId);
          const nestedItems = renderPrerequisiteTreeItems(prerequisiteId, branch, allEdges);
          return `<li>${{link}}${{relation}}${{nestedItems ? `<ul class="prereq-tree">${{nestedItems}}</ul>` : ''}}</li>`;
        }}).join('');
      }}

      function focusAndInspect(nodeId) {{
        inspectNode(nodeId);
        if (WORKED_EXAMPLES[nodeId]) {{
          highlightWorkedExampleStep();
          return;
        }}
        highlightNodeNeighborhood(nodeId);
        network.focus(nodeId, {{
          scale: 1.15,
          animation: {{ duration: 650, easingFunction: 'easeInOutCubic' }}
        }});
      }}

      // Switch between neutral pastel nodes and course-specific pastel colors.
      function setVisualTheme(mode) {{
        currentTheme = mode;
        document.getElementById('theme-constellation').classList.toggle('active', mode === 'constellation');
        document.getElementById('theme-course').classList.toggle('active', mode === 'course');

        const nodeUpdates = Object.keys(NODE_META).map(nid => {{
          const m = NODE_META[nid];
          if (mode === 'constellation') {{
            const isHub = Boolean(m.badge);
            return {{
              id: nid,
              color: {{
                background: '#fffdf9',
                border: m.color,
                highlight: {{ background: '#f2d9dc', border: '#ba7e88' }},
                hover: {{ background: m.color, border: '#8390a3' }}
              }},
              shadow: {{
                enabled: true,
                color: 'rgba(100, 112, 132, 0.20)',
                size: isHub ? 10 : 6
              }}
            }};
          }} else {{
            return {{
              id: nid,
              color: {{
                background: m.color,
                border: '#ffffff',
                highlight: {{ background: '#f2d9dc', border: '#ba7e88' }},
                hover: {{ background: m.color, border: '#8390a3' }}
              }},
              shadow: {{
                enabled: true,
                color: m.color,
                size: 8
              }}
            }};
          }}
        }});
        nodes.update(nodeUpdates);
      }}

      // Highlight a clicked node's immediate 1-hop neighborhood and show edge relationships
      function highlightNodeNeighborhood(centerId) {{
        const allEdges = edges.get();
        const connectedEdges = allEdges.filter(e => e.from === centerId || e.to === centerId);
        const neighborIds = new Set([centerId]);
        connectedEdges.forEach(e => {{
          neighborIds.add(e.from);
          neighborIds.add(e.to);
        }});

        const nodeUpdates = nodes.get().map(n => {{
          const isFocus = neighborIds.has(n.id);
          return {{
            id: n.id,
            opacity: isFocus ? 1.0 : 0.32,
            font: {{ color: isFocus ? '#384455' : '#8994a5', size: 13 }}
          }};
        }});
        nodes.update(nodeUpdates);

        const edgeUpdates = allEdges.map(e => {{
          const isConn = (e.from === centerId || e.to === centerId);
          return {{
            id: e.id,
            label: isConn ? (e.rel_text || '') : '',
            width: isConn ? 2.6 : 1.0,
            color: {{
              color: isConn ? '#c9828e' : 'rgba(91, 105, 127, 0.08)'
            }},
            font: {{ size: 11, color: '#526074', background: 'rgba(255,255,255,0.90)', strokeWidth: 0 }}
          }};
        }});
        edges.update(edgeUpdates);
      }}

      // Activate a Guided Mathematical Thread for step-by-step follow-through
      function activateThread(threadKey) {{
        activeThreadKey = threadKey;
        activeStepIdx = 0;
        const thread = THREADS[threadKey];
        if (!thread) return;

        document.querySelectorAll('.thread-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('th-' + threadKey).classList.add('active');

        const seqSet = new Set(thread.sequence);
        const nodeUpdates = nodes.get().map(n => {{
          const inThread = seqSet.has(n.id);
          return {{
            id: n.id,
            hidden: false,
            opacity: inThread ? 1.0 : 0.32,
            font: {{ color: inThread ? '#384455' : '#8994a5', size: 13 }}
          }};
        }});
        nodes.update(nodeUpdates);

        const edgeUpdates = edges.get().map(e => {{
          const inChain = seqSet.has(e.from) && seqSet.has(e.to);
          return {{
            id: e.id,
            label: inChain ? (e.rel_text || '') : '',
            width: inChain ? 3.0 : 0.8,
            color: {{
              color: inChain ? thread.color : 'rgba(91, 105, 127, 0.08)'
            }},
            font: {{ size: 11, color: '#526074', background: 'rgba(255,255,255,0.90)', strokeWidth: 0 }}
          }};
        }});
        edges.update(edgeUpdates);

        document.getElementById('stepper-panel').style.display = 'block';
        focusThreadStep();
      }}

      function stepThread(delta) {{
        if (!activeThreadKey) return;
        const seq = THREADS[activeThreadKey].sequence;
        activeStepIdx = (activeStepIdx + delta + seq.length) % seq.length;
        focusThreadStep();
      }}

      function focusThreadStep() {{
        const thread = THREADS[activeThreadKey];
        const currentId = thread.sequence[activeStepIdx];
        const meta = NODE_META[currentId];
        document.getElementById('stepper-title').textContent = thread.name;
        document.getElementById('stepper-progress').textContent =
          `Step ${{activeStepIdx + 1}} of ${{thread.sequence.length}}: ${{meta.label}}`;

        inspectNode(currentId);
        network.selectNodes([currentId]);
        network.focus(currentId, {{
          scale: 1.12,
          animation: {{ duration: 650, easingFunction: 'easeInOutCubic' }}
        }});
      }}

      function resetHighlight() {{
        activeThreadKey = null;
        document.querySelectorAll('.thread-btn').forEach(b => b.classList.remove('active'));
        document.getElementById('stepper-panel').style.display = 'none';

        setVisualTheme(currentTheme);
        nodes.update(nodes.get().map(n => ({{
          id: n.id,
          opacity: 1.0,
          font: {{ color: '#384455', size: 13 }}
        }})));

        edges.update(edges.get().map(e => {{
          const isCross = NODE_META[e.from].group !== NODE_META[e.to].group;
          return {{
            id: e.id,
            label: '',
            width: isCross ? 1.5 : 1.1,
            color: {{ color: isCross ? 'rgba(91, 105, 127, 0.20)' : 'rgba(91, 105, 127, 0.28)' }}
          }};
        }}));
      }}

      function filterCourse(courseGroup) {{
        document.querySelectorAll('[id^="flt-"]').forEach(b => b.classList.remove('active'));
        const btn = document.getElementById('flt-' + courseGroup);
        if (btn) btn.classList.add('active');

        const updates = nodes.get().map(n => ({{
          id: n.id,
          hidden: (courseGroup !== 'ALL' && n.group !== courseGroup)
        }}));
        nodes.update(updates);
        network.fit({{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
      }}

      function togglePhysicsFreeze() {{
        physicsFrozen = !physicsFrozen;
        network.setOptions({{ physics: {{ enabled: !physicsFrozen }} }});
        const btn = document.getElementById('btn-freeze');
        btn.classList.toggle('active', physicsFrozen);
        btn.textContent = physicsFrozen ? 'Unfreeze Layout' : 'Freeze Layout';
      }}

      function togglePyvisConfig() {{
        const cfg = document.getElementById('config');
        if (!cfg) return;
        cfg.style.display = (cfg.style.display === 'block') ? 'none' : 'block';
      }}

      window.addEventListener('load', function() {{
        setTimeout(initConstellationGraph, 150);
      }});
    </script>
    """

    with open(output_filename, "r", encoding="utf-8") as f:
        html_content = f.read()

    if not html_content.lstrip().lower().startswith("<!doctype html"):
      html_content = "<!DOCTYPE html>\n" + html_content

    if "</body>" in html_content:
        html_content = html_content.replace("</body>", f"{custom_enhancement}\n</body>")
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)

    print(f"Successfully generated constellation graph: '{output_filename}'")


if __name__ == "__main__":
    calc_graph, metadata = build_calculus_digraph()
    print(
        f"Graph initialized with {calc_graph.number_of_nodes()} nodes "
        f"and {calc_graph.number_of_edges()} directed edges."
    )
    create_interactive_network(calc_graph, metadata, "calculus_network.html")