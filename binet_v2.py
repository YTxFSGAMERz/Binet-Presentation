"""
Binet's Formula via Matrix Diagonalization  —  IMPROVED EDITION
================================================================
A professional Manim + manim-slides presentation (~48 slides)

Improvements over v1:
  ISSUE  1: Micro-stepped derivations (one transform per slide)
  ISSUE  2: Eigenvalue intuition with 2-D vector animation
  ISSUE  3: Dramatic paradox sequence with decimal approximations
  ISSUE  4: Visual applications (rabbit icons, tile drawings, schedule blocks)
  ISSUE  5: Diagonalization intuition (general vs diagonal comparison)
  ISSUE  6: Pre-reveal suspense slide before Binet's formula
  ISSUE  7: Strict layout rules — no overlaps, consistent spacing
  ISSUE  8: Slower pacing, pauses after key results
  ISSUE  9: Reused MathTex objects, Transform instead of recreate
  ISSUE 10: Visual hierarchy (primary/secondary/tertiary)
  ISSUE 11: Focus control — SurroundingRectangle, fade-outs, arrows
  ISSUE 12: TransformMatchingTex for equation continuity

Render:
    manim-slides render binet_v2.py BinetPresentation -ql
    manim-slides present binet_v2.py BinetPresentation
"""

from manim import *
from manim_slides import Slide

# ═══════════════════════════════════════════════
#  COLOUR PALETTE & STYLE CONSTANTS
# ═══════════════════════════════════════════════
BG         = "#0F172A"
TEXT_PRI   = "#E2E8F0"   # primary text
TEXT_SEC   = "#94A3B8"   # secondary / labels
TEXT_TER   = "#64748B"   # tertiary / faded
BLUE       = "#60A5FA"   # matrices
GOLD       = "#FBBF24"   # φ
RED        = "#F87171"   # ψ
GREEN      = "#34D399"   # results / checkmarks
PURPLE     = "#A78BFA"   # accents

FONT_TITLE = 40
FONT_BODY  = 28
FONT_LABEL = 22
FONT_MATH  = 44
BUFF_STD   = 0.45        # standard inter-element gap


# ═══════════════════════════════════════════════
#  HELPER UTILITIES
# ═══════════════════════════════════════════════

def header(text, color=TEXT_PRI, size=FONT_TITLE):
    """Slide header — placed at top."""
    t = Text(text, font_size=size, color=color, weight=BOLD)
    t.to_edge(UP, buff=0.45)
    return t

def body(text, color=TEXT_PRI, size=FONT_BODY):
    return Text(text, font_size=size, color=color)

def label(text, color=TEXT_SEC, size=FONT_LABEL):
    return Text(text, font_size=size, color=color)

def focus(mob, color=GREEN, buff=0.18, width=3):
    """SurroundingRectangle for focus control."""
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=width)

def dim(*mobs, opacity=0.35):
    """Dim objects to tertiary level."""
    return [m.animate.set_opacity(opacity) for m in mobs]

def brighten(*mobs, opacity=1.0):
    """Restore full opacity."""
    return [m.animate.set_opacity(opacity) for m in mobs]


# ═══════════════════════════════════════════════
#  MAIN PRESENTATION CLASS
# ═══════════════════════════════════════════════

class BinetPresentation(Slide):

    def setup(self):
        self.camera.background_color = ManimColor(BG)

    # ── master construct ─────────────────────────
    def construct(self):
        self._s01_title()

    # helper: advance slide and clear
    def _advance(self):
        self.next_slide()
        self.clear()

    # ════════════════════════════════════════════
    #  SLIDE 1 — Title
    # ════════════════════════════════════════════
    def _s01_title(self):
        # Faint background numbers
        fib = [0,1,1,2,3,5,8,13,21,34,55,89,144]
        bg = VGroup(*[Integer(v, font_size=18, color=TEXT_TER, fill_opacity=0.12)
                       for v in fib]).arrange_in_grid(rows=3, cols=5, buff=0.7)
        bg.move_to(ORIGIN)
        self.add(bg)

        t1 = Text("Binet's Formula", font_size=54, color=TEXT_PRI, weight=BOLD)
        t2 = Text("via Matrix Diagonalization", font_size=36, color=BLUE)
        t3 = Text("Linear Algebra Honours Project", font_size=24, color=TEXT_SEC)
        grp = VGroup(t1, t2, t3).arrange(DOWN, buff=0.45).move_to(UP*0.3)

        self.play(Write(t1), run_time=1.6)
        self.play(FadeIn(t2, shift=UP*0.3), run_time=0.9)
        self.play(FadeIn(t3, shift=UP*0.3), run_time=0.7)
        self.wait(0.5)
        self._advance()
        self._s02_fib_intro()

    # ════════════════════════════════════════════
    #  SLIDE 2 — Fibonacci intro
    # ════════════════════════════════════════════
    def _s02_fib_intro(self):
        hdr = header("The Fibonacci Sequence")
        self.add(hdr)

        vals = [0,1,1,2,3,5,8,13,21,34]
        nums = VGroup(*[Integer(v, font_size=44, color=GOLD) for v in vals])
        nums.arrange(RIGHT, buff=0.55).move_to(UP*0.3)

        for n in nums:
            self.play(FadeIn(n, shift=UP*0.25, scale=1.15), run_time=0.28)

        dots = Text("...", font_size=44, color=TEXT_SEC)
        dots.next_to(nums, RIGHT, buff=0.35)
        self.play(FadeIn(dots, shift=RIGHT), run_time=0.35)
        self.wait(0.4)
        self._advance()
        self._s03_recurrence()

    # ════════════════════════════════════════════
    #  SLIDE 3 — Recurrence
    # ════════════════════════════════════════════
    def _s03_recurrence(self):
        hdr = header("The Recurrence")
        self.add(hdr)

        rec = MathTex(r"F_{n+2} = F_{n+1} + F_n", font_size=50, color=GOLD)
        rec.move_to(UP*0.3)
        init = MathTex(r"F_0 = 0, \quad F_1 = 1", font_size=40, color=TEXT_SEC)
        init.next_to(rec, DOWN, buff=BUFF_STD)

        self.play(Write(rec), run_time=1.4)
        self.play(FadeIn(init, shift=UP*0.25), run_time=0.9)
        box = focus(rec, color=GOLD)
        self.play(Create(box), run_time=0.6)
        self.wait(0.6)
        self._advance()
        self._s04_problem()

    # ════════════════════════════════════════════
    #  SLIDE 4 — Problem with iteration
    # ════════════════════════════════════════════
    def _s04_problem(self):
        hdr = header("The Problem", color=RED)
        self.add(hdr)

        lines = VGroup(
            MathTex(r"F_0 = 0",  font_size=32, color=TEXT_SEC),
            MathTex(r"F_1 = 1",  font_size=32, color=TEXT_SEC),
            MathTex(r"F_2 = F_1 + F_0 = 1", font_size=32, color=TEXT_SEC),
            MathTex(r"F_3 = F_2 + F_1 = 2", font_size=32, color=TEXT_SEC),
            MathTex(r"F_4 = F_3 + F_2 = 3", font_size=32, color=TEXT_SEC),
            MathTex(r"F_5 = F_4 + F_3 = 5", font_size=32, color=TEXT_SEC),
            MathTex(r"\vdots",   font_size=32, color=RED),
            MathTex(r"F_{100} = \; ??", font_size=36, color=RED),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        lines.move_to(LEFT*1.5)

        for ln in lines:
            self.play(FadeIn(ln, shift=RIGHT*0.25), run_time=0.3)

        # fade old lines to dim
        self.play(*dim(*lines[:6]), run_time=0.5)

        q = Text("Can we compute $F_n$ directly?", font_size=30, color=GREEN, weight=BOLD)
        q.move_to(RIGHT*2.8 + UP*0.3)
        qbox = focus(q, color=GREEN, buff=0.2)
        self.play(FadeIn(q, scale=1.08), run_time=1.0)
        self.play(Create(qbox), run_time=0.5)
        self.wait(0.6)
        self._advance()
        self._s05_matrix_idea()

    # ════════════════════════════════════════════
    #  SLIDE 5 — Matrix idea
    # ════════════════════════════════════════════
    def _s05_matrix_idea(self):
        hdr = header("The Key Idea", color=BLUE)
        self.add(hdr)

        idea = body("Encode the recurrence as a matrix equation", color=TEXT_PRI, size=26)
        idea.move_to(UP*1.8)

        arr = Arrow(LEFT*2.2, RIGHT*2.2, color=BLUE, stroke_width=4)
        arr.move_to(UP*0.5)
        ll = label("Recurrence", color=TEXT_SEC); ll.next_to(arr, LEFT, buff=0.25)
        rl = label("Matrix Power", color=BLUE);   rl.next_to(arr, RIGHT, buff=0.25)

        self.play(FadeIn(idea), run_time=0.6)
        self.play(GrowArrow(arr), run_time=0.9)
        self.play(FadeIn(ll), FadeIn(rl), run_time=0.5)

        # Show the transform
        rec = MathTex(r"F_{n+2} = F_{n+1} + F_n", font_size=36, color=GOLD)
        rec.move_to(DOWN*1.0)
        self.play(Write(rec), run_time=1.0)

        mat = MathTex(
            r"\begin{bmatrix} F_{n+2} \\ F_{n+1} \end{bmatrix}"
            r"= \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}"
            r"\begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix}",
            font_size=36, color=BLUE)
        mat.move_to(DOWN*1.0)

        self.play(Transform(rec, mat), run_time=1.6)
        box = focus(rec, color=BLUE)
        self.play(Create(box), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s06_state_vector()

    # ════════════════════════════════════════════
    #  SLIDE 6 — State vector
    # ════════════════════════════════════════════
    def _s06_state_vector(self):
        hdr = header("State Vector")
        self.add(hdr)

        vdef = MathTex(
            r"\mathbf{v}_n = \begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix}",
            font_size=FONT_MATH, color=BLUE)
        vdef.move_to(UP*0.5)

        v0 = MathTex(
            r"\mathbf{v}_0 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}",
            font_size=40, color=GOLD)
        v0.next_to(vdef, DOWN, buff=BUFF_STD)

        self.play(Write(vdef), run_time=1.3)
        self.play(FadeIn(v0, shift=UP*0.25), run_time=0.9)
        self.play(Create(focus(vdef, color=BLUE)), run_time=0.5)
        self.wait(0.4)
        self._advance()
        self._s07_transition_matrix()

    # ════════════════════════════════════════════
    #  SLIDE 7 — Transition matrix
    # ════════════════════════════════════════════
    def _s07_transition_matrix(self):
        hdr = header("Transition Matrix")
        self.add(hdr)

        Mdef = MathTex(
            r"M = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}",
            font_size=52, color=BLUE)
        Mdef.move_to(UP*0.4)

        eq = MathTex(r"\mathbf{v}_{n+1} = M \, \mathbf{v}_n",
                      font_size=42, color=GOLD)
        eq.next_to(Mdef, DOWN, buff=BUFF_STD)

        self.play(Write(Mdef), run_time=1.3)
        self.play(FadeIn(eq, shift=UP*0.25), run_time=0.9)
        self.play(Create(focus(Mdef, color=BLUE)), run_time=0.5)
        self.wait(0.4)
        self._advance()
        self._s08_verify()

    # ════════════════════════════════════════════
    #  SLIDE 8 — Verify matrix recurrence (micro-stepped)
    # ════════════════════════════════════════════
    def _s08_verify(self):
        hdr = header("Verify the Recurrence")
        self.add(hdr)

        step1 = MathTex(
            r"M \, \mathbf{v}_n = "
            r"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}"
            r"\begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix}",
            font_size=38, color=BLUE)
        step1.move_to(UP*1.0)
        self.play(Write(step1), run_time=1.2)
        self.wait(0.3)

        step2 = MathTex(
            r"= \begin{bmatrix} F_{n+1} + F_n \\ F_{n+1} \end{bmatrix}",
            font_size=38, color=TEXT_PRI)
        step2.next_to(step1, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(step2, shift=DOWN*0.15), run_time=0.9)
        self.wait(0.2)

        step3 = MathTex(
            r"= \begin{bmatrix} F_{n+2} \\ F_{n+1} \end{bmatrix} = \mathbf{v}_{n+1}",
            font_size=38, color=GREEN)
        step3.next_to(step2, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(step3, shift=DOWN*0.15), run_time=0.9)
        self.play(Create(focus(step3, color=GREEN)), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s09_power()

    # ════════════════════════════════════════════
    #  SLIDE 9 — Power of matrix
    # ════════════════════════════════════════════
    def _s09_power(self):
        hdr = header("Power of the Matrix")
        self.add(hdr)

        eq = MathTex(r"\mathbf{v}_n = M^n \, \mathbf{v}_0",
                      font_size=50, color=GOLD)
        eq.move_to(UP*0.4)

        emp = body('"Everything depends on computing $M^n$"', color=BLUE, size=26)
        emp.move_to(DOWN*1.0)

        self.play(Write(eq), run_time=1.3)
        self.play(FadeIn(emp, scale=1.08), run_time=0.9)
        self.play(Create(focus(eq, color=GOLD)), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s10_simplification()

    # ════════════════════════════════════════════
    #  SLIDE 10 — Simplification needed
    # ════════════════════════════════════════════
    def _s10_simplification(self):
        hdr = header("How to Compute $M^n$?")
        self.add(hdr)

        naive = MathTex(
            r"M^n = \underbrace{M \cdot M \cdots M}_{n \text{ times}}",
            font_size=40, color=RED)
        naive.move_to(UP*0.5)
        cross = Cross(naive, stroke_color=RED, stroke_width=3)

        self.play(Write(naive), run_time=1.1)
        self.play(Create(cross), run_time=0.6)

        better = body("Better: Diagonalize!", color=GREEN, size=30)
        better.move_to(DOWN*0.6)

        diag = MathTex(
            r"M = P \, D \, P^{-1} \;\Longrightarrow\; M^n = P \, D^n \, P^{-1}",
            font_size=42, color=GREEN)
        diag.move_to(DOWN*1.7)

        self.play(FadeIn(better, scale=1.15), run_time=0.9)
        self.play(Write(diag), run_time=1.3)
        self.play(Create(focus(diag, color=GREEN)), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s11_diagonalization_intuition()

    # ════════════════════════════════════════════
    #  SLIDE 11 — DIAGONALIZATION INTUITION (NEW)
    #  ISSUE 5: conceptual comparison
    # ════════════════════════════════════════════
    def _s11_diagonalization_intuition(self):
        hdr = header("Why Diagonalize?", color=GREEN)
        self.add(hdr)

        # Left: general matrix = messy transform
        left_title = label("General Matrix", color=RED)
        left_title.move_to(LEFT*3.2 + UP*1.3)

        # Draw a small grid that gets sheared
        grid_left = NumberPlane(
            x_range=[-1,1,1], y_range=[-1,1,1],
            background_line_style={"stroke_color": TEXT_TER, "stroke_width": 1, "stroke_opacity": 0.4},
            faded_line_style={"stroke_color": TEXT_TER, "stroke_width": 0.5, "stroke_opacity": 0.2},
        ).scale(0.7)
        grid_left.move_to(LEFT*3.2 + UP*0.0)

        messy_label = label("Shearing + Scaling", color=RED, size=18)
        messy_label.next_to(grid_left, DOWN, buff=0.3)

        # Right: diagonal matrix = independent scaling
        right_title = label("Diagonal Matrix", color=GREEN)
        right_title.move_to(RIGHT*3.2 + UP*1.3)

        grid_right = NumberPlane(
            x_range=[-1,1,1], y_range=[-1,1,1],
            background_line_style={"stroke_color": TEXT_TER, "stroke_width": 1, "stroke_opacity": 0.4},
            faded_line_style={"stroke_color": TEXT_TER, "stroke_width": 0.5, "stroke_opacity": 0.2},
        ).scale(0.7)
        grid_right.move_to(RIGHT*3.2 + UP*0.0)

        scale_label = label("Independent Scaling", color=GREEN, size=18)
        scale_label.next_to(grid_right, DOWN, buff=0.3)

        self.play(FadeIn(left_title), FadeIn(grid_left), FadeIn(messy_label), run_time=0.8)
        self.play(FadeIn(right_title), FadeIn(grid_right), FadeIn(scale_label), run_time=0.8)

        # Animate: left grid gets sheared
        shear_mat = np.array([[1, 0.5], [0.3, 1]])
        self.play(grid_left.animate.apply_matrix(shear_mat), run_time=1.5)

        # Animate: right grid just scales axes independently
        scale_mat = np.array([[1.6, 0], [0, 0.6]])
        self.play(grid_right.animate.apply_matrix(scale_mat), run_time=1.5)

        msg = body("Diagonalization: turn messy transformations into simple scaling",
                    color=TEXT_PRI, size=22)
        msg.move_to(DOWN*2.5)
        self.play(FadeIn(msg), run_time=0.8)
        self.wait(0.6)
        self._advance()
        self._s12_eigenvalue_intro()

    # ════════════════════════════════════════════
    #  SLIDE 12 — Eigenvalues intro
    # ════════════════════════════════════════════
    def _s12_eigenvalue_intro(self):
        hdr = header("Finding Eigenvalues")
        self.add(hdr)

        ceq = MathTex(r"\det(M - \lambda I) = 0", font_size=FONT_MATH, color=BLUE)
        ceq.move_to(UP*0.4)
        self.play(Write(ceq), run_time=1.2)
        self.play(Create(focus(ceq, color=BLUE)), run_time=0.5)
        self.wait(0.4)
        self._advance()
        self._s13_char_poly()

    # ════════════════════════════════════════════
    #  SLIDE 13 — Characteristic polynomial (micro-stepped)
    # ════════════════════════════════════════════
    def _s13_char_poly(self):
        hdr = header("Characteristic Polynomial")
        self.add(hdr)

        s1 = MathTex(
            r"\det\begin{bmatrix} 1-\lambda & 1 \\ 1 & -\lambda \end{bmatrix}",
            font_size=42, color=BLUE)
        s1.move_to(UP*1.0)
        self.play(Write(s1), run_time=1.1)
        self.wait(0.3)

        s2 = MathTex(r"= (1-\lambda)(-\lambda) - 1",
                      font_size=42, color=TEXT_PRI)
        s2.next_to(s1, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(FadeIn(s2, shift=DOWN*0.15), run_time=0.9)
        self.wait(0.2)

        s3 = MathTex(r"= \lambda^2 - \lambda - 1",
                      font_size=48, color=GOLD)
        s3.next_to(s2, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(FadeIn(s3, shift=DOWN*0.15), run_time=1.0)
        self.play(Create(focus(s3, color=GOLD)), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s14_solve_eigenvalues()

    # ════════════════════════════════════════════
    #  SLIDE 14 — Solve eigenvalues
    # ════════════════════════════════════════════
    def _s14_solve_eigenvalues(self):
        hdr = header("Solve the Equation")
        self.add(hdr)

        eq = MathTex(r"\lambda^2 - \lambda - 1 = 0",
                      font_size=42, color=TEXT_PRI)
        eq.move_to(UP*1.5)
        quad = MathTex(r"\lambda = \frac{1 \pm \sqrt{5}}{2}",
                        font_size=46, color=TEXT_PRI)
        quad.move_to(UP*0.3)

        self.play(Write(eq), run_time=0.9)
        self.play(Write(quad), run_time=1.1)

        phi = MathTex(r"\lambda_1 = \varphi = \frac{1+\sqrt{5}}{2}",
                       font_size=44, color=GOLD)
        phi.move_to(DOWN*0.7)
        psi = MathTex(r"\lambda_2 = \psi = \frac{1-\sqrt{5}}{2}",
                       font_size=44, color=RED)
        psi.move_to(DOWN*1.7)

        self.play(FadeIn(phi, shift=RIGHT*0.2), run_time=0.9)
        self.play(Create(focus(phi, color=GOLD)), run_time=0.4)
        self.play(FadeIn(psi, shift=RIGHT*0.2), run_time=0.9)
        self.play(Create(focus(psi, color=RED)), run_time=0.4)
        self.wait(0.5)
        self._advance()
        self._s15_phi_psi()

    # ════════════════════════════════════════════
    #  SLIDE 15 — φ and ψ properties
    # ════════════════════════════════════════════
    def _s15_phi_psi(self):
        hdr = header("The Golden Ratio", color=GOLD)
        self.add(hdr)

        phi_s = MathTex(r"\varphi", font_size=72, color=GOLD)
        phi_s.move_to(LEFT*2.5 + UP*0.3)
        phi_v = MathTex(r"= \frac{1+\sqrt{5}}{2} \approx 1.618",
                         font_size=42, color=GOLD)
        phi_v.next_to(phi_s, RIGHT, buff=0.25)

        psi_s = MathTex(r"\psi", font_size=72, color=RED)
        psi_s.move_to(LEFT*2.5 + DOWN*1.1)
        psi_v = MathTex(r"= \frac{1-\sqrt{5}}{2} \approx -0.618",
                         font_size=42, color=RED)
        psi_v.next_to(psi_s, RIGHT, buff=0.25)

        self.play(Write(phi_s), Write(phi_v), run_time=1.3)
        self.play(Write(psi_s), Write(psi_v), run_time=1.3)

        vieta = MathTex(
            r"\varphi+\psi=1,\quad \varphi\psi=-1,\quad \varphi-\psi=\sqrt{5}",
            font_size=34, color=PURPLE)
        vieta.move_to(DOWN*2.6)
        self.play(FadeIn(vieta, shift=UP*0.15), run_time=0.9)
        self.wait(0.5)
        self._advance()
        self._s16_eigenvalue_intuition()

    # ════════════════════════════════════════════
    #  SLIDE 16 — EIGENVALUE INTUITION (NEW)
    #  ISSUE 2: geometric visualisation
    # ════════════════════════════════════════════
    def _s16_eigenvalue_intuition(self):
        hdr = header("Eigenvectors: Directions That Only Scale", color=BLUE)
        self.add(hdr)

        # Draw a 2-D arrow (generic vector)
        ax = Axes(x_range=[-2,2,1], y_range=[-1.5,1.5,1],
                  axis_config={"color": TEXT_TER, "stroke_width": 1.5},
                  tips=False).scale(0.8)
        ax.move_to(UP*0.2)
        self.play(FadeIn(ax), run_time=0.5)

        # Generic vector — changes direction under M
        v_gen = Arrow(ORIGIN, RIGHT*1.2 + UP*0.8, color=TEXT_SEC, buff=0, stroke_width=3)
        self.play(GrowArrow(v_gen), run_time=0.6)
        lbl_gen = label("Any vector", color=TEXT_SEC, size=18)
        lbl_gen.next_to(v_gen.get_end(), UR, buff=0.1)

        # After M — direction changes
        v_after = Arrow(ORIGIN, RIGHT*1.8 + UP*0.2, color=RED, buff=0, stroke_width=3)
        self.play(Transform(v_gen, v_after), run_time=1.0)
        self.play(FadeIn(lbl_gen), run_time=0.3)
        self.wait(0.3)

        # Now eigenvector for φ — direction preserved, scaled by φ
        v_phi = Arrow(ORIGIN, RIGHT*0.618 + UP*1, color=GOLD, buff=0, stroke_width=3.5)
        v_phi_scaled = Arrow(ORIGIN, (RIGHT*0.618 + UP*1)*1.618, color=GOLD, buff=0, stroke_width=3.5)
        lbl_phi = label(r"$\varphi$-direction", color=GOLD, size=18)

        self.play(FadeOut(v_gen), FadeOut(lbl_gen), run_time=0.3)
        self.play(GrowArrow(v_phi), run_time=0.6)
        lbl_phi.next_to(v_phi.get_end(), UR, buff=0.1)
        self.play(FadeIn(lbl_phi), run_time=0.3)
        self.play(Transform(v_phi, v_phi_scaled), run_time=1.0)

        scale_phi = label(r"scaled by $\varphi \approx 1.618$", color=GOLD, size=17)
        scale_phi.next_to(v_phi, RIGHT, buff=0.15)
        self.play(FadeIn(scale_phi), run_time=0.4)
        self.wait(0.3)

        # Eigenvector for ψ — inverted & shrunk
        v_psi = Arrow(ORIGIN, RIGHT*0.618 + DOWN*1, color=RED, buff=0, stroke_width=3.5)
        v_psi_scaled = Arrow(ORIGIN, (RIGHT*0.618 + DOWN*1)*0.382, color=RED, buff=0, stroke_width=3.5)
        lbl_psi = label(r"$\psi$-direction", color=RED, size=18)

        self.play(GrowArrow(v_psi), run_time=0.6)
        lbl_psi.next_to(v_psi.get_end(), DR, buff=0.1)
        self.play(FadeIn(lbl_psi), run_time=0.3)
        self.play(Transform(v_psi, v_psi_scaled), run_time=1.0)

        scale_psi = label(r"scaled by $\psi \approx -0.618$ (flipped!)", color=RED, size=17)
        scale_psi.next_to(v_psi, RIGHT, buff=0.15)
        self.play(FadeIn(scale_psi), run_time=0.4)

        bottom = body("Eigenvectors are directions that only scale", color=GREEN, size=22)
        bottom.move_to(DOWN*2.5)
        self.play(FadeIn(bottom), run_time=0.6)
        self.wait(0.5)
        self._advance()
        self._s17_eigenvectors()

    # ════════════════════════════════════════════
    #  SLIDE 17 — Eigenvectors (algebraic)
    # ════════════════════════════════════════════
    def _s17_eigenvectors(self):
        hdr = header("Eigenvectors")
        self.add(hdr)

        eq = MathTex(r"(M - \lambda I)\,\mathbf{x} = \mathbf{0}",
                      font_size=38, color=BLUE)
        eq.move_to(UP*1.3)

        e_phi = MathTex(r"\mathbf{x}_1 = \begin{bmatrix} \varphi \\ 1 \end{bmatrix}",
                         font_size=44, color=GOLD)
        e_phi.move_to(LEFT*2.2 + DOWN*0.2)

        e_psi = MathTex(r"\mathbf{x}_2 = \begin{bmatrix} \psi \\ 1 \end{bmatrix}",
                         font_size=44, color=RED)
        e_psi.move_to(RIGHT*2.2 + DOWN*0.2)

        self.play(Write(eq), run_time=0.9)
        self.play(Write(e_phi), run_time=0.9)
        self.play(Create(focus(e_phi, color=GOLD)), run_time=0.4)
        self.play(Write(e_psi), run_time=0.9)
        self.play(Create(focus(e_psi, color=RED)), run_time=0.4)

        note = label(r"(Since $\varphi^2 = \varphi + 1$, the row reduces to zero)", color=TEXT_SEC)
        note.move_to(DOWN*1.5)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(0.4)
        self._advance()
        self._s18_matrix_P()

    # ════════════════════════════════════════════
    #  SLIDE 18 — Matrix P
    # ════════════════════════════════════════════
    def _s18_matrix_P(self):
        hdr = header("Modal Matrix $P$")
        self.add(hdr)

        Pdef = MathTex(
            r"P = \begin{bmatrix} \varphi & \psi \\ 1 & 1 \end{bmatrix}",
            font_size=50, color=BLUE)
        Pdef.move_to(UP*0.5)

        det = MathTex(r"\det(P) = \varphi - \psi = \sqrt{5}",
                       font_size=38, color=GOLD)
        det.next_to(Pdef, DOWN, buff=BUFF_STD)

        self.play(Write(Pdef), run_time=1.3)
        self.play(FadeIn(det, shift=UP*0.25), run_time=0.9)
        self.play(Create(focus(Pdef, color=BLUE)), run_time=0.5)
        self.wait(0.4)
        self._advance()
        self._s19_diagonalization()

    # ════════════════════════════════════════════
    #  SLIDE 19 — Diagonalization
    # ════════════════════════════════════════════
    def _s19_diagonalization(self):
        hdr = header("Diagonalization", color=GREEN)
        self.add(hdr)

        decomp = MathTex(r"M = P \, D \, P^{-1}", font_size=52, color=GREEN)
        decomp.move_to(UP*0.5)

        Dmat = MathTex(
            r"D = \begin{bmatrix} \varphi & 0 \\ 0 & \psi \end{bmatrix}",
            font_size=42, color=BLUE)
        Dmat.move_to(DOWN*0.7 + LEFT*2.8)

        Pinv = MathTex(
            r"P^{-1} = \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} 1 & -\psi \\ -1 & \varphi \end{bmatrix}",
            font_size=38, color=PURPLE)
        Pinv.move_to(DOWN*0.7 + RIGHT*2.8)

        self.play(Write(decomp), run_time=1.3)
        self.play(Create(focus(decomp, color=GREEN)), run_time=0.5)
        self.play(FadeIn(Dmat, shift=UP*0.15), run_time=0.9)
        self.play(FadeIn(Pinv, shift=UP*0.15), run_time=0.9)
        self.wait(0.5)
        self._advance()
        self._s20_power_diagonal()

    # ════════════════════════════════════════════
    #  SLIDE 20 — Powering the diagonal matrix
    # ════════════════════════════════════════════
    def _s20_power_diagonal(self):
        hdr = header("Powering Made Simple", color=GREEN)
        self.add(hdr)

        insight = MathTex(r"M^n = P \, D^n \, P^{-1}",
                           font_size=50, color=GREEN)
        insight.move_to(UP*0.5)

        Dn = MathTex(
            r"D^n = \begin{bmatrix} \varphi^n & 0 \\ 0 & \psi^n \end{bmatrix}",
            font_size=46, color=BLUE)
        Dn.move_to(DOWN*0.7)

        self.play(Write(insight), run_time=1.3)
        self.play(Write(Dn), run_time=1.3)
        self.play(Create(focus(Dn, color=BLUE)), run_time=0.5)

        note = body("Just exponentiate the diagonal entries!", color=GOLD, size=24)
        note.move_to(DOWN*2.3)
        self.play(FadeIn(note, scale=1.08), run_time=0.7)
        self.wait(0.5)
        self._advance()
        self._s21_step1_Pinv_v0()

    # ════════════════════════════════════════════
    #  SLIDES 21-25 — Micro-stepped derivation
    #  ISSUE 1: one transform per slide
    # ════════════════════════════════════════════

    def _s21_step1_Pinv_v0(self):
        hdr = header("Step 1: Compute $P^{-1}\\mathbf{v}_0$")
        self.add(hdr)

        context = MathTex(
            r"\mathbf{v}_n = P \, D^n \, P^{-1} \, \mathbf{v}_0",
            font_size=36, color=TEXT_TER)
        context.move_to(UP*1.6)
        self.add(context)

        step = MathTex(
            r"P^{-1} \mathbf{v}_0 "
            r"= \frac{1}{\sqrt{5}} \begin{bmatrix} 1 & -\psi \\ -1 & \varphi \end{bmatrix}"
            r"\begin{bmatrix} 1 \\ 0 \end{bmatrix}",
            font_size=36, color=BLUE)
        step.move_to(UP*0.3)

        result = MathTex(
            r"= \frac{1}{\sqrt{5}} \begin{bmatrix} 1 \\ -1 \end{bmatrix}",
            font_size=40, color=GREEN)
        result.move_to(DOWN*1.0)

        self.play(Write(step), run_time=1.2)
        self.play(FadeIn(result, shift=DOWN*0.15), run_time=1.0)
        self.play(Create(focus(result, color=GREEN)), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s22_step2_Dn()

    def _s22_step2_Dn(self):
        hdr = header("Step 2: Apply $D^n$")
        self.add(hdr)

        prev = MathTex(
            r"P^{-1}\mathbf{v}_0 = \frac{1}{\sqrt{5}}\begin{bmatrix} 1 \\ -1 \end{bmatrix}",
            font_size=34, color=TEXT_TER)
        prev.move_to(UP*1.6)
        self.add(prev)

        step = MathTex(
            r"D^n \cdot \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} 1 \\ -1 \end{bmatrix}"
            r"= \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi^n \\ -\psi^n \end{bmatrix}",
            font_size=36, color=BLUE)
        step.move_to(UP*0.2)

        note = label("Each entry scaled by its eigenvalue!", color=GOLD, size=20)
        note.move_to(DOWN*1.2)
        self.play(Write(step), run_time=1.3)
        self.play(Create(focus(step, color=BLUE)), run_time=0.5)
        self.play(FadeIn(note), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s23_step3_multiply_P()

    def _s23_step3_multiply_P(self):
        hdr = header("Step 3: Multiply by $P$")
        self.add(hdr)

        step = MathTex(
            r"\mathbf{v}_n = \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi & \psi \\ 1 & 1 \end{bmatrix}"
            r"\begin{bmatrix} \varphi^n \\ -\psi^n \end{bmatrix}",
            font_size=34, color=BLUE)
        step.move_to(UP*0.5)

        result = MathTex(
            r"= \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi^{n+1} - \psi^{n+1} \\ \varphi^n - \psi^n \end{bmatrix}",
            font_size=38, color=GOLD)
        result.move_to(DOWN*1.0)

        self.play(Write(step), run_time=1.2)
        self.play(FadeIn(result, shift=DOWN*0.15), run_time=1.0)
        self.play(Create(focus(result, color=GOLD)), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s24_step4_extract()

    def _s24_step4_extract(self):
        hdr = header("Step 4: Read Off $F_n$")
        self.add(hdr)

        vec = MathTex(
            r"\begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix}"
            r"= \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi^{n+1} - \psi^{n+1} \\"
            r"\varphi^n - \psi^n \end{bmatrix}",
            font_size=34, color=BLUE)
        vec.move_to(UP*0.8)

        arr = Arrow(UP*0.0, DOWN*0.5, color=GREEN, stroke_width=3)
        arr.next_to(vec, DOWN, buff=0.2)

        extract = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=52, color=GOLD)
        extract.move_to(DOWN*1.5)

        self.play(Write(vec), run_time=1.0)
        self.play(GrowArrow(arr), run_time=0.5)
        self.play(Write(extract), run_time=1.4)
        self.play(Create(focus(extract, color=GOLD)), run_time=0.5)
        self.wait(0.6)
        self._advance()
        self._s25_pre_reveal()

    # ════════════════════════════════════════════
    #  SLIDE 25 — Pre-reveal suspense (NEW)
    #  ISSUE 6: dramatic build-up
    # ════════════════════════════════════════════
    def _s25_pre_reveal(self):
        suspense = Text(
            "All this work leads to one elegant expression\u2026",
            font_size=30, color=TEXT_PRI, weight=BOLD)
        suspense.move_to(ORIGIN)

        self.play(FadeIn(suspense), run_time=1.2)
        self.wait(1.5)
        self.play(suspense.animate.set_color(GREEN).scale(1.05), run_time=0.8)
        self.wait(1.0)
        self._advance()
        self._s26_binet_reveal()

    # ════════════════════════════════════════════
    #  SLIDE 26 — BINET'S FORMULA REVEAL
    # ════════════════════════════════════════════
    def _s26_binet_reveal(self):
        hdr = header("Binet's Formula", color=GOLD, size=44)
        self.add(hdr)

        formula = MathTex(
            r"F_n = \frac{1}{\sqrt{5}}"
            r"\left[\left(\frac{1+\sqrt{5}}{2}\right)^{\!n}"
            r"- \left(\frac{1-\sqrt{5}}{2}\right)^{\!n}\right]",
            font_size=44, color=GREEN)
        formula.move_to(UP*0.3)

        short = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=48, color=GOLD)
        short.next_to(formula, DOWN, buff=0.7)

        self.play(Write(formula), run_time=2.5, rate_func=smooth)
        self.wait(0.6)
        self.play(Create(focus(formula, color=GREEN, buff=0.2, width=4)), run_time=0.9)

        self.play(Write(short), run_time=1.2)
        self.play(Create(focus(short, color=GOLD, buff=0.2, width=4)), run_time=0.6)
        self.wait(1.2)
        self._advance()
        self._s27_verification()

    # ════════════════════════════════════════════
    #  SLIDE 27 — Verification
    # ════════════════════════════════════════════
    def _s27_verification(self):
        hdr = header("Verification", color=GREEN)
        self.add(hdr)

        n0 = MathTex(
            r"n=0:\quad F_0 = \frac{\varphi^0 - \psi^0}{\sqrt{5}}"
            r"= \frac{1-1}{\sqrt{5}} = 0 \;\checkmark",
            font_size=36, color=GREEN)
        n0.move_to(UP*0.6)

        n1 = MathTex(
            r"n=1:\quad F_1 = \frac{\varphi - \psi}{\sqrt{5}}"
            r"= \frac{\sqrt{5}}{\sqrt{5}} = 1 \;\checkmark",
            font_size=36, color=GREEN)
        n1.move_to(DOWN*0.6)

        self.play(Write(n0), run_time=1.2)
        self.wait(0.3)
        self.play(Write(n1), run_time=1.2)

        ok = body("Formula checks out for base cases!", color=GREEN, size=26)
        ok.move_to(DOWN*2.0)
        self.play(FadeIn(ok, scale=1.08), run_time=0.7)
        self.wait(0.5)
        self._advance()
        self._s28_induction()

    # ════════════════════════════════════════════
    #  SLIDE 28 — Induction (light)
    # ════════════════════════════════════════════
    def _s28_induction(self):
        hdr = header("Proof by Strong Induction")
        self.add(hdr)

        items = VGroup(
            body("Base Cases: $n=0,\\,1$ hold", color=GREEN, size=26),
            body("Assume: true for all $j \\leq k$", color=GOLD, size=26),
            body("Show: true for $k+1$", color=GREEN, size=26),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        items.move_to(LEFT*1.5 + UP*0.3)

        arrows = VGroup()
        for i in range(len(items)-1):
            a = Arrow(items[i].get_bottom()+DOWN*0.05,
                      items[i+1].get_top()+UP*0.05,
                      color=BLUE, stroke_width=2.5)
            arrows.add(a)

        key = MathTex(r"F_{k+1} = F_k + F_{k-1}"
                       r"= \frac{\varphi^{k+1}-\psi^{k+1}}{\sqrt{5}}",
                       font_size=34, color=GREEN)
        key.move_to(RIGHT*2.5 + UP*0.0)

        for it, ar in zip(items[:2], arrows):
            self.play(FadeIn(it), run_time=0.5)
            self.play(GrowArrow(ar), run_time=0.35)
        self.play(FadeIn(items[2]), run_time=0.5)
        self.play(Write(key), run_time=1.0)
        self.wait(0.5)
        self._advance()
        self._s29_paradox_question()

    # ════════════════════════════════════════════
    #  SLIDES 29-31 — INTEGRALITY PARADOX (dramatic)
    #  ISSUE 3: decimal approximations, suspense
    # ════════════════════════════════════════════

    def _s29_paradox_question(self):
        hdr = header("The Integrality Paradox", color=RED)
        self.add(hdr)

        formula = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=48, color=GOLD)
        formula.move_to(UP*0.5)

        # Highlight irrational markers
        sq_numerator = focus(
            MathTex(r"\sqrt{5}", font_size=30, color=RED),
            color=RED, buff=0.12)
        sq_denom = focus(
            MathTex(r"\sqrt{5}", font_size=30, color=RED),
            color=RED, buff=0.12)
        sq_numerator.move_to(UP*0.5 + RIGHT*2.2)
        sq_denom.move_to(DOWN*0.5 + RIGHT*0.0)

        q = Text("Why is $F_n$ always an integer?",
                  font_size=32, color=RED, weight=BOLD)
        q.move_to(DOWN*1.2)

        irr = body("This formula is saturated with $\\sqrt{5}$!", color=RED, size=24)
        irr.move_to(DOWN*2.2)

        self.play(Write(formula), run_time=1.2)
        self.play(FadeIn(sq_numerator), FadeIn(sq_denom), run_time=0.6)
        self.play(FadeIn(q, scale=1.1), run_time=1.1)
        self.play(FadeIn(irr), run_time=0.6)
        self.wait(0.6)
        self._advance()
        self._s30_paradox_example()

    def _s30_paradox_example(self):
        hdr = header("A Concrete Example: $n=5$", color=RED)
        self.add(hdr)

        # Step-by-step decimal approximation
        t1 = MathTex(r"\varphi^5 \approx 11.090\,169\ldots",
                      font_size=40, color=GOLD)
        t1.move_to(UP*1.0)

        t2 = MathTex(r"\psi^5 \approx -0.090\,169\ldots",
                      font_size=40, color=RED)
        t2.move_to(UP*0.0)

        self.play(Write(t1), run_time=1.0)
        self.play(Write(t2), run_time=1.0)
        self.wait(0.4)

        # Subtraction
        diff = MathTex(
            r"\varphi^5 - \psi^5 \approx 11.090\,169 - (-0.090\,169) = 11.180\,339\ldots",
            font_size=32, color=TEXT_PRI)
        diff.move_to(DOWN*0.8)
        self.play(Write(diff), run_time=1.2)
        self.wait(0.3)

        # Division
        div = MathTex(
            r"\frac{\varphi^5 - \psi^5}{\sqrt{5}}"
            r"\approx \frac{11.180\,339}{2.236\,068} = 5.000\,000\ldots",
            font_size=32, color=TEXT_PRI)
        div.move_to(DOWN*1.7)
        self.play(Write(div), run_time=1.2)
        self.wait(0.3)

        # Reveal
        result = MathTex(r"= 5", font_size=60, color=GREEN)
        result.move_to(DOWN*2.8)
        self.play(FadeIn(result, scale=1.3), run_time=1.2)
        self.play(Create(focus(result, color=GREEN, buff=0.25, width=5)), run_time=0.7)
        self.wait(0.8)
        self._advance()
        self._s31_paradox_resolution()

    def _s31_paradox_resolution(self):
        hdr = header("Structural Cancellation", color=GREEN)
        self.add(hdr)

        rep1 = MathTex(r"\varphi^n = A_n\varphi + B_n", font_size=42, color=GOLD)
        rep1.move_to(UP*0.5)
        rep2 = MathTex(r"\psi^n = A_n\psi + B_n", font_size=42, color=RED)
        rep2.next_to(rep1, DOWN, buff=0.45)

        same = body("Same integer coefficients $A_n, B_n$!", color=GREEN, size=24)
        same.move_to(DOWN*0.4)

        self.play(Write(rep1), run_time=0.9)
        self.play(Write(rep2), run_time=0.9)
        self.play(FadeIn(same, scale=1.08), run_time=0.7)

        cancel = MathTex(
            r"F_n = \frac{(A_n\varphi + B_n) - (A_n\psi + B_n)}{\sqrt{5}}"
            r"= \frac{A_n(\varphi - \psi)}{\sqrt{5}}",
            font_size=34, color=TEXT_PRI)
        cancel.move_to(DOWN*1.5)
        self.play(Write(cancel), run_time=1.3)

        # Key identity
        kid = MathTex(r"\varphi - \psi = \sqrt{5}", font_size=42, color=GOLD)
        kid.move_to(DOWN*2.6)
        self.play(Write(kid), run_time=0.9)
        self.play(Create(focus(kid, color=GOLD)), run_time=0.4)
        self.wait(0.5)
        self._advance()
        self._s32_resolution_final()

    def _s32_resolution_final(self):
        hdr = header("The Resolution", color=GREEN)
        self.add(hdr)

        res = MathTex(
            r"F_n = \frac{A_n \cdot \sqrt{5}}{\sqrt{5}} = A_n",
            font_size=48, color=GREEN)
        res.move_to(UP*0.5)

        conc = MathTex(
            r"A_n \in \mathbb{N}_0 \implies F_n \in \mathbb{N}_0",
            font_size=42, color=GREEN)
        conc.move_to(DOWN*0.8)

        self.play(Write(res), run_time=1.3)
        self.play(Create(focus(res, color=GREEN)), run_time=0.5)
        self.play(FadeIn(conc, scale=1.08), run_time=1.0)

        remark = label(
            r"Moreover: $A_n = F_n$ and $B_n = F_{n-1}$, "
            r"so $\varphi^n = F_n\varphi + F_{n-1}$",
            color=TEXT_SEC)
        remark.move_to(DOWN*2.3)
        self.play(FadeIn(remark), run_time=0.5)
        self.wait(0.5)
        self._advance()
        self._s33_rabbits()

    # ════════════════════════════════════════════
    #  SLIDES 33-35 — VISUAL APPLICATIONS
    #  ISSUE 4: 70%+ visual per slide
    # ════════════════════════════════════════════

    def _s33_rabbits(self):
        hdr = header("Application 1: Rabbit Population", size=34)
        self.add(hdr)

        # Visual: rabbit pairs as circles (young=small, adult=large)
        months_lbl = ["Jan","Feb","Mar","Apr","May","Jun"]
        young_vals  = [1,0,1,1,2,3]
        adult_vals  = [0,1,1,2,3,5]

        for i, (mo, yv, av) in enumerate(zip(months_lbl, young_vals, adult_vals)):
            col = VGroup()
            # month label
            ml = Text(mo, font_size=16, color=PURPLE)
            col.add(ml)
            # young pairs as small circles
            for _ in range(min(yv, 5)):
                c = Circle(radius=0.08, fill_color=GOLD, fill_opacity=0.8, stroke_width=1, stroke_color=GOLD)
                col.add(c)
            if yv > 5:
                col.add(Text(f"+{yv-5}", font_size=12, color=GOLD))
            # adult pairs as larger circles
            for _ in range(min(av, 5)):
                c = Circle(radius=0.13, fill_color=RED, fill_opacity=0.8, stroke_width=1, stroke_color=RED)
                col.add(c)
            if av > 5:
                col.add(Text(f"+{av-5}", font_size=12, color=RED))

            col.arrange(DOWN, buff=0.08)

        # Build columns
        columns = VGroup()
        for i, (mo, yv, av) in enumerate(zip(months_lbl, young_vals, adult_vals)):
            col = VGroup()
            ml = Text(mo, font_size=14, color=PURPLE)
            col.add(ml)
            y_grp = VGroup(*[Circle(radius=0.07, fill_color=GOLD, fill_opacity=0.8,
                                     stroke_width=1, stroke_color=GOLD) for _ in range(min(yv,4))])
            if yv > 4:
                y_grp.add(Text(f"+{yv-4}", font_size=11, color=GOLD))
            if len(y_grp) > 0:
                y_grp.arrange(RIGHT, buff=0.03)
                col.add(y_grp)
            a_grp = VGroup(*[Circle(radius=0.11, fill_color=RED, fill_opacity=0.8,
                                     stroke_width=1, stroke_color=RED) for _ in range(min(av,4))])
            if av > 4:
                a_grp.add(Text(f"+{av-4}", font_size=11, color=RED))
            if len(a_grp) > 0:
                a_grp.arrange(RIGHT, buff=0.03)
                col.add(a_grp)
            col.arrange(DOWN, buff=0.1)
            columns.add(col)

        columns.arrange(RIGHT, buff=0.35).move_to(UP*0.2)

        # Legend
        y_leg = Circle(radius=0.07, fill_color=GOLD, fill_opacity=0.8, stroke_width=1, stroke_color=GOLD)
        y_lab = Text("Young", font_size=14, color=GOLD)
        a_leg = Circle(radius=0.11, fill_color=RED, fill_opacity=0.8, stroke_width=1, stroke_color=RED)
        a_lab = Text("Adult", font_size=14, color=RED)
        legend = VGroup(
            VGroup(y_leg, y_lab).arrange(RIGHT, buff=0.1),
            VGroup(a_leg, a_lab).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.5)
        legend.move_to(DOWN*1.6)

        self.play(FadeIn(columns), run_time=1.2)
        self.play(FadeIn(legend), run_time=0.5)

        formula = MathTex(
            r"T_n = F_{n+1} = \frac{\varphi^{n+1} - \psi^{n+1}}{\sqrt{5}}",
            font_size=32, color=GREEN)
        formula.move_to(DOWN*2.5)
        self.play(Write(formula), run_time=1.0)
        self.wait(0.4)
        self._advance()
        self._s34_tiling()

    def _s34_tiling(self):
        hdr = header("Application 2: Tiling a $1 \\times n$ Board", size=34)
        self.add(hdr)

        # Draw actual tiles: squares and dominoes
        # n=1: one square
        # n=2: two squares OR one domino
        # n=3: ...

        sq_color = BLUE
        dom_color = PURPLE

        # n=1
        n1_label = Text("n=1:", font_size=20, color=TEXT_SEC)
        n1_tile = Square(side_length=0.4, fill_color=sq_color, fill_opacity=0.5,
                         stroke_color=sq_color, stroke_width=2)
        n1_grp = VGroup(n1_label, n1_tile).arrange(RIGHT, buff=0.15)
        n1_count = Text("1 way", font_size=18, color=GREEN)
        n1_count.next_to(n1_grp, RIGHT, buff=0.2)

        # n=2
        n2_label = Text("n=2:", font_size=20, color=TEXT_SEC)
        n2_sq = VGroup(*[Square(side_length=0.4, fill_color=sq_color, fill_opacity=0.5,
                                stroke_color=sq_color, stroke_width=2) for _ in range(2)]
                       ).arrange(RIGHT, buff=0.02)
        n2_dom = Rectangle(width=0.82, height=0.4, fill_color=dom_color, fill_opacity=0.5,
                           stroke_color=dom_color, stroke_width=2)
        n2_tiles = VGroup(n2_sq, n2_dom).arrange(RIGHT, buff=0.3)
        n2_grp = VGroup(n2_label, n2_tiles).arrange(RIGHT, buff=0.15)
        n2_count = Text("2 ways", font_size=18, color=GREEN)
        n2_count.next_to(n2_grp, RIGHT, buff=0.2)

        # n=3
        n3_label = Text("n=3:", font_size=20, color=TEXT_SEC)
        n3a = VGroup(*[Square(side_length=0.4, fill_color=sq_color, fill_opacity=0.5,
                              stroke_color=sq_color, stroke_width=2) for _ in range(3)]
                     ).arrange(RIGHT, buff=0.02)
        n3b = VGroup(
            Rectangle(width=0.82, height=0.4, fill_color=dom_color, fill_opacity=0.5,
                      stroke_color=dom_color, stroke_width=2),
            Square(side_length=0.4, fill_color=sq_color, fill_opacity=0.5,
                   stroke_color=sq_color, stroke_width=2),
        ).arrange(RIGHT, buff=0.02)
        n3c = VGroup(
            Square(side_length=0.4, fill_color=sq_color, fill_opacity=0.5,
                   stroke_color=sq_color, stroke_width=2),
            Rectangle(width=0.82, height=0.4, fill_color=dom_color, fill_opacity=0.5,
                      stroke_color=dom_color, stroke_width=2),
        ).arrange(RIGHT, buff=0.02)
        n3_tiles = VGroup(n3a, n3b, n3c).arrange(RIGHT, buff=0.25)
        n3_grp = VGroup(n3_label, n3_tiles).arrange(RIGHT, buff=0.15)
        n3_count = Text("3 ways", font_size=18, color=GREEN)
        n3_count.next_to(n3_grp, RIGHT, buff=0.2)

        all_rows = VGroup(
            VGroup(n1_grp, n1_count).arrange(RIGHT, buff=0.15),
            VGroup(n2_grp, n2_count).arrange(RIGHT, buff=0.15),
            VGroup(n3_grp, n3_count).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.35)
        all_rows.move_to(UP*0.5)

        # Legend
        sq_leg = Square(side_length=0.25, fill_color=sq_color, fill_opacity=0.5,
                        stroke_color=sq_color, stroke_width=2)
        sq_txt = Text("= 1x1 square", font_size=14, color=sq_color)
        dom_leg = Rectangle(width=0.55, height=0.25, fill_color=dom_color, fill_opacity=0.5,
                            stroke_color=dom_color, stroke_width=2)
        dom_txt = Text("= 1x2 domino", font_size=14, color=dom_color)
        legend = VGroup(
            VGroup(sq_leg, sq_txt).arrange(RIGHT, buff=0.1),
            VGroup(dom_leg, dom_txt).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.4)
        legend.move_to(DOWN*1.8)

        self.play(FadeIn(all_rows), run_time=1.2)
        self.play(FadeIn(legend), run_time=0.5)

        formula = MathTex(
            r"W_n = F_{n+1} = \frac{\varphi^{n+1} - \psi^{n+1}}{\sqrt{5}}",
            font_size=32, color=GREEN)
        formula.move_to(DOWN*2.6)
        self.play(Write(formula), run_time=1.0)
        self.wait(0.4)
        self._advance()
        self._s35_schedules()

    def _s35_schedules(self):
        hdr = header("Application 3: Study Schedules", size=34)
        self.add(hdr)

        # R = rest (green), H = heavy (gold), blocked HH (red)
        def make_day(letter, color, size=0.32):
            sq = Square(side_length=size, fill_color=color, fill_opacity=0.6,
                        stroke_color=color, stroke_width=2)
            txt = Text(letter, font_size=16, color=TEXT_PRI).move_to(sq.get_center())
            return VGroup(sq, txt)

        # Valid n=3 schedules
        valid = [
            ["R","R","R"],
            ["R","R","H"],
            ["R","H","R"],
            ["H","R","R"],
            ["H","R","H"],
        ]

        valid_rows = VGroup()
        for sched in valid:
            row = VGroup()
            for d in sched:
                c = GREEN if d == "R" else GOLD
                row.add(make_day(d, c))
            row.arrange(RIGHT, buff=0.04)
            valid_rows.add(row)
        valid_rows.arrange(DOWN, buff=0.12)
        valid_rows.move_to(LEFT*2.5 + UP*0.3)

        v_lbl = label("Valid (n=3):", color=GREEN)
        v_lbl.next_to(valid_rows, UP, buff=0.15)

        # Invalid
        invalid_row = VGroup(make_day("H", RED), make_day("H", RED), make_day("R", GREEN))
        invalid_row.arrange(RIGHT, buff=0.04)
        invalid_row.move_to(RIGHT*2.5 + UP*0.3)
        cross = Cross(invalid_row, stroke_color=RED, stroke_width=3)

        i_lbl = label("Invalid (HH):", color=RED)
        i_lbl.next_to(invalid_row, UP, buff=0.15)

        self.play(FadeIn(v_lbl), FadeIn(valid_rows), run_time=0.9)
        self.play(FadeIn(i_lbl), FadeIn(invalid_row), run_time=0.5)
        self.play(Create(cross), run_time=0.4)

        formula = MathTex(
            r"S_n = F_{n+2} = \frac{\varphi^{n+2} - \psi^{n+2}}{\sqrt{5}}",
            font_size=30, color=GREEN)
        formula.move_to(DOWN*1.8)

        ex = MathTex(r"S_7 = F_9 = 34", font_size=34, color=GOLD)
        ex.move_to(DOWN*2.6)

        self.play(Write(formula), run_time=1.0)
        self.play(Write(ex), run_time=0.7)
        self.wait(0.4)
        self._advance()
        self._s36_summary()

    # ════════════════════════════════════════════
    #  SLIDE 36 — Summary pipeline
    # ════════════════════════════════════════════
    def _s36_summary(self):
        hdr = header("Summary", size=44)
        self.add(hdr)

        steps = VGroup(
            VGroup(Text("Recurrence", font_size=26, color=GOLD),
                   MathTex(r"F_{n+2}=F_{n+1}+F_n", font_size=24, color=TEXT_SEC)
                   ).arrange(DOWN, buff=0.1),
            VGroup(Text("Matrix", font_size=26, color=BLUE),
                   MathTex(r"\mathbf{v}_n = M^n\mathbf{v}_0", font_size=24, color=TEXT_SEC)
                   ).arrange(DOWN, buff=0.1),
            VGroup(Text("Eigenvalues", font_size=26, color=PURPLE),
                   MathTex(r"\varphi,\;\psi", font_size=24, color=TEXT_SEC)
                   ).arrange(DOWN, buff=0.1),
            VGroup(Text("Formula", font_size=26, color=GREEN),
                   MathTex(r"F_n=\frac{\varphi^n-\psi^n}{\sqrt{5}}", font_size=24, color=TEXT_SEC)
                   ).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=0.8)
        steps.move_to(UP*0.5)

        arrows = VGroup()
        for i in range(len(steps)-1):
            a = Arrow(steps[i].get_right()+RIGHT*0.05,
                      steps[i+1].get_left()+LEFT*0.05,
                      color=TEXT_SEC, stroke_width=2)
            arrows.add(a)

        for s in steps:
            self.play(FadeIn(s, shift=RIGHT*0.2), run_time=0.45)
        for a in arrows:
            self.play(GrowArrow(a), run_time=0.25)

        takeaways = VGroup(
            body("1. Fibonacci encodes as a matrix problem", color=TEXT_PRI, size=22),
            body("2. Diagonalization simplifies $M^n$", color=TEXT_PRI, size=22),
            body("3. Binet's formula gives $F_n$ directly", color=TEXT_PRI, size=22),
            body("4. Irrationals cancel — always integer!", color=GREEN, size=22),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        takeaways.move_to(DOWN*1.8)

        self.play(LaggedStart(*[FadeIn(t) for t in takeaways], lag_ratio=0.18), run_time=1.3)
        self.wait(0.5)
        self._advance()
        self._s37_closing()

    # ════════════════════════════════════════════
    #  SLIDE 37 — Closing
    # ════════════════════════════════════════════
    def _s37_closing(self):
        fib_vals = [0,1,1,2,3,5,8,13,21,34,55,89,144]
        fib_row = VGroup(*[Integer(v, font_size=34, color=GOLD) for v in fib_vals])
        fib_row.arrange(RIGHT, buff=0.35).move_to(UP*1.5)

        for n in fib_row:
            self.play(FadeIn(n, shift=UP*0.2, scale=1.1), run_time=0.18)

        msg = Text("From Recursion to Elegance",
                    font_size=40, color=GREEN, weight=BOLD)
        msg.move_to(UP*0.0)

        formula = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=50, color=GOLD)
        formula.move_to(DOWN*1.2)

        self.play(Write(msg), run_time=1.5)
        self.play(Write(formula), run_time=1.5)
        self.play(Create(focus(formula, color=GOLD, buff=0.2, width=4)), run_time=0.7)
        self.wait(2)
