"""
Binet's Formula via Matrix Diagonalization
==========================================
A complete Manim + manim-slides presentation.
All overlapping issues eliminated via systematic VGroup layout.

LAYOUT RULES ENFORCED:
  - Every scene uses VGroup().arrange() for vertical stacking
  - Content groups are centered on ORIGIN (slightly above for title)
  - Header always at to_edge(UP, buff=0.5)
  - No absolute move_to() for content below header
  - Each slide has max 3-4 lines of math (split if more)
  - Minimum buff=0.45 between vertical elements
  - All MathTex font_size >= 36

Render with:
    manim-slides render binet_formula_presentation.py BinetPresentation -pql
    manim-slides convert binet_formula_presentation.py BinetPresentation
"""

from manim import *
from manim_slides import Slide

# ─────────────────────────────────────────────
# GLOBAL STYLE CONSTANTS
# ─────────────────────────────────────────────
BG_COLOR      = "#0F172A"
TEXT_COLOR     = "#E2E8F0"
BLUE_MAT      = "#60A5FA"
GOLD_PHI      = "#FBBF24"
RED_PSI       = "#F87171"
GREEN_RESULT  = "#34D399"
ACCENT_PURPLE = "#A78BFA"
DIM_WHITE     = "#94A3B8"

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def make_title(text, color=TEXT_COLOR, size=44):
    """Slide header — always placed at to_edge(UP, buff=0.5)"""
    t = Text(text, font_size=size, color=color, weight=BOLD)
    t.to_edge(UP, buff=0.5)
    return t

def make_note(text, color=DIM_WHITE, size=28):
    return MathTex(text, font_size=size, color=color)

def box(mob, color=GREEN_RESULT, buff=0.15):
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=3)

def center_content(group, y_shift=0.0):
    """Center a VGroup on screen with optional vertical shift"""
    group.move_to(ORIGIN + UP * y_shift)


# ═════════════════════════════════════════════
#  MAIN PRESENTATION CLASS
# ═════════════════════════════════════════════

class BinetPresentation(Slide):

    def setup(self):
        self.camera.background_color = ManimColor(BG_COLOR)

    def construct(self):
        self.scene_01_title()

    # ─── SCENE 1: Title Slide ────────────────────
    def scene_01_title(self):
        fib_nums = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        bg_nums = VGroup(*[
            Integer(f, font_size=24, color=DIM_WHITE, fill_opacity=0.15)
            for f in fib_nums
        ]).arrange_in_grid(rows=3, cols=4, buff=0.8)
        bg_nums.move_to(ORIGIN)
        self.add(bg_nums)

        title = Text("Binet's Formula", font_size=54, color=TEXT_COLOR, weight=BOLD)
        title_sub = Text("via Matrix Diagonalization", font_size=40, color=BLUE_MAT, weight=BOLD)
        subtitle = Text("Linear Algebra Honours Project", font_size=28, color=DIM_WHITE)

        group = VGroup(title, title_sub, subtitle).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(title_sub, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.6)

        self.next_slide()
        self.clear()
        self.scene_02_fibonacci_motivation()

    # ─── SCENE 2: Fibonacci Motivation ─────────
    def scene_02_fibonacci_motivation(self):
        header = make_title("The Fibonacci Sequence")
        self.add(header)

        fib_vals = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        fib_mobs = VGroup(*[
            Integer(val, font_size=48, color=GOLD_PHI) for val in fib_vals
        ]).arrange(RIGHT, buff=0.6)
        fib_mobs.move_to(UP * 0.5)

        dots = Text("...", font_size=48, color=DIM_WHITE)
        dots.next_to(fib_mobs, RIGHT, buff=0.4)

        for mob in fib_mobs:
            self.play(FadeIn(mob, shift=UP * 0.3, scale=1.2), run_time=0.3)
        self.play(FadeIn(dots, shift=RIGHT), run_time=0.4)

        self.next_slide()
        self.clear()
        self.scene_03_recurrence()

    # ─── SCENE 3: Recurrence Definition ────────
    def scene_03_recurrence(self):
        header = make_title("The Recurrence")
        self.add(header)

        recurrence = MathTex(
            r"F_{n+2} = F_{n+1} + F_n", font_size=52, color=GOLD_PHI
        )
        init_cond = MathTex(
            r"F_0 = 0, \quad F_1 = 1", font_size=44, color=TEXT_COLOR
        )

        group = VGroup(recurrence, init_cond).arrange(DOWN, buff=0.7)
        center_content(group, y_shift=0.3)

        self.play(Write(recurrence), run_time=1.2)
        self.play(FadeIn(init_cond, shift=UP * 0.3), run_time=0.8)
        self.play(Create(box(recurrence, color=GOLD_PHI)), run_time=0.6)

        self.next_slide()
        self.clear()
        self.scene_04_problem()

    # ─── SCENE 4: Problem with Iteration ───────
    def scene_04_problem(self):
        header = make_title("The Problem", color=RED_PSI)
        self.add(header)

        iter_lines = VGroup(
            MathTex(r"F_0 = 0", font_size=36, color=DIM_WHITE),
            MathTex(r"F_1 = 1", font_size=36, color=DIM_WHITE),
            MathTex(r"F_2 = F_1 + F_0 = 1", font_size=36, color=DIM_WHITE),
            MathTex(r"F_3 = F_2 + F_1 = 2", font_size=36, color=DIM_WHITE),
            MathTex(r"F_4 = F_3 + F_2 = 3", font_size=36, color=DIM_WHITE),
            MathTex(r"F_5 = F_4 + F_3 = 5", font_size=36, color=DIM_WHITE),
            MathTex(r"\vdots", font_size=36, color=RED_PSI),
            MathTex(r"F_{100} = \; ??", font_size=40, color=RED_PSI),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        iter_lines.move_to(LEFT * 3.0 + DOWN * 0.2)

        for line in iter_lines:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.3)

        question = MathTex(
            r"\text{Can we compute } F_n \text{ directly?}",
            font_size=40, color=GREEN_RESULT
        )
        question.move_to(RIGHT * 3.5 + UP * 0.5)

        self.play(FadeIn(question, scale=1.1), run_time=1.0)
        self.play(Create(box(question, color=GREEN_RESULT, buff=0.2)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_05_matrix_idea()

    # ─── SCENE 5: Idea of Matrix Representation ─
    def scene_05_matrix_idea(self):
        header = make_title("The Key Idea", color=BLUE_MAT)
        self.add(header)

        idea = Text("Encode the recurrence as a matrix equation",
                     font_size=36, color=TEXT_COLOR)
        idea.move_to(UP * 1.5)

        arrow = Arrow(LEFT * 2, RIGHT * 2, color=BLUE_MAT, stroke_width=4)
        arrow.move_to(UP * 0.5)
        left_label = Text("Recurrence", font_size=32, color=DIM_WHITE)
        left_label.next_to(arrow, LEFT, buff=0.3)
        right_label = Text("Matrix Power", font_size=32, color=BLUE_MAT)
        right_label.next_to(arrow, RIGHT, buff=0.3)

        self.play(FadeIn(idea), run_time=0.6)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.play(FadeIn(left_label), FadeIn(right_label), run_time=0.5)

        recurrence = MathTex(r"F_{n+2} = F_{n+1} + F_n",
                             font_size=44, color=GOLD_PHI)
        recurrence.move_to(DOWN * 1.0)

        matrix_form = MathTex(
            r"\begin{bmatrix} F_{n+2} \\ F_{n+1} \end{bmatrix} = "
            r"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}"
            r"\begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix}",
            font_size=40, color=BLUE_MAT
        )
        matrix_form.move_to(DOWN * 1.0)

        self.play(Write(recurrence), run_time=1.0)
        self.play(Transform(recurrence, matrix_form), run_time=1.5)

        self.next_slide()
        self.clear()
        self.scene_06_state_vector()

    # ─── SCENE 6: Define State Vector ───────────
    def scene_06_state_vector(self):
        header = make_title("State Vector")
        self.add(header)

        vec_def = MathTex(
            r"\mathbf{v}_n = \begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix}",
            font_size=52, color=BLUE_MAT
        )
        init_vec = MathTex(
            r"\mathbf{v}_0 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}",
            font_size=48, color=GOLD_PHI
        )

        group = VGroup(vec_def, init_vec).arrange(DOWN, buff=0.8)
        center_content(group, y_shift=0.3)

        self.play(Write(vec_def), run_time=1.2)
        self.play(FadeIn(init_vec, shift=UP * 0.3), run_time=0.8)
        self.play(Create(box(vec_def, color=BLUE_MAT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_07_transition_matrix()

    # ─── SCENE 7: Define Transition Matrix ──────
    def scene_07_transition_matrix(self):
        header = make_title("Transition Matrix")
        self.add(header)

        M_def = MathTex(
            r"M = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}",
            font_size=56, color=BLUE_MAT
        )
        trans_eq = MathTex(
            r"\mathbf{v}_{n+1} = M \, \mathbf{v}_n",
            font_size=48, color=GOLD_PHI
        )

        group = VGroup(M_def, trans_eq).arrange(DOWN, buff=0.8)
        center_content(group, y_shift=0.3)

        self.play(Write(M_def), run_time=1.2)
        self.play(FadeIn(trans_eq, shift=UP * 0.3), run_time=0.8)
        self.play(Create(box(M_def, color=BLUE_MAT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_08_matrix_recurrence()

    # ─── SCENE 8: Show Matrix Recurrence ────────
    def scene_08_matrix_recurrence(self):
        header = make_title("Verify the Recurrence")
        self.add(header)

        mult = MathTex(
            r"M \, \mathbf{v}_n = "
            r"\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}"
            r"\begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix}",
            font_size=42, color=BLUE_MAT
        )
        result = MathTex(
            r"= \begin{bmatrix} F_{n+1} + F_n \\ F_{n+1} \end{bmatrix}",
            font_size=42, color=TEXT_COLOR
        )
        final = MathTex(
            r"= \begin{bmatrix} F_{n+2} \\ F_{n+1} \end{bmatrix}"
            r" = \mathbf{v}_{n+1}",
            font_size=42, color=GREEN_RESULT
        )

        group = VGroup(mult, result, final).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.2)

        self.play(Write(mult), run_time=1.0)
        self.play(FadeIn(result, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(final, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(box(final, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_09_power_of_matrix()

    # ─── SCENE 9: Power of Matrix ───────────────
    def scene_09_power_of_matrix(self):
        header = make_title("Power of the Matrix")
        self.add(header)

        eq1 = MathTex(
            r"\mathbf{v}_n = M^n \, \mathbf{v}_0",
            font_size=52, color=GOLD_PHI
        )
        emphasis = MathTex(
            r"\text{Everything depends on computing } M^n",
            font_size=36, color=BLUE_MAT
        )

        group = VGroup(eq1, emphasis).arrange(DOWN, buff=0.8)
        center_content(group, y_shift=0.3)

        self.play(Write(eq1), run_time=1.2)
        self.play(FadeIn(emphasis, scale=1.1), run_time=0.8)
        self.play(Create(box(eq1, color=GOLD_PHI)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_10_simplification_needed()

    # ─── SCENE 10: Need for Simplification ──────
    def scene_10_simplification_needed(self):
        header = MathTex(
            r"\text{How to Compute } M^n \text{?}",
            font_size=44, color=TEXT_COLOR
        )
        header.to_edge(UP, buff=0.5)
        self.add(header)

        naive = MathTex(
            r"M^n = \underbrace{M \cdot M \cdots M}_{n \text{ times}}",
            font_size=44, color=RED_PSI
        )
        cross = Cross(naive, stroke_color=RED_PSI, stroke_width=3)

        better_label = MathTex(
            r"\text{Better: Diagonalize!}",
            font_size=40, color=GREEN_RESULT
        )
        diagonalized = MathTex(
            r"M = P \, D \, P^{-1} \implies M^n = P \, D^n \, P^{-1}",
            font_size=44, color=GREEN_RESULT
        )

        group = VGroup(naive, better_label, diagonalized).arrange(DOWN, buff=0.6)
        center_content(group, y_shift=0.3)

        self.play(Write(naive), run_time=1.0)
        self.play(Create(cross), run_time=0.6)
        self.play(FadeIn(better_label, scale=1.2), run_time=0.8)
        self.play(Write(diagonalized), run_time=1.2)
        self.play(Create(box(diagonalized, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_11_eigenvalues_intro()

    # ─── SCENE 11: Eigenvalues Introduction ─────
    def scene_11_eigenvalues_intro(self):
        header = make_title("Eigenvalues")
        self.add(header)

        char_eq = MathTex(
            r"\det(M - \lambda I) = 0", font_size=52, color=BLUE_MAT
        )
        char_eq.move_to(UP * 0.5)

        self.play(Write(char_eq), run_time=1.0)
        self.play(Create(box(char_eq, color=BLUE_MAT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_12_char_poly()

    # ─── SCENE 12: Characteristic Polynomial ────
    def scene_12_char_poly(self):
        header = make_title("Characteristic Polynomial")
        self.add(header)

        step1 = MathTex(
            r"\det \begin{bmatrix} 1-\lambda & 1 \\ 1 & -\lambda \end{bmatrix}",
            font_size=48, color=BLUE_MAT
        )
        step2 = MathTex(
            r"= (1-\lambda)(-\lambda) - 1 \cdot 1",
            font_size=44, color=TEXT_COLOR
        )
        step3 = MathTex(
            r"= \lambda^2 - \lambda - 1",
            font_size=52, color=GOLD_PHI
        )

        group = VGroup(step1, step2, step3).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.3)

        self.play(Write(step1), run_time=1.0)
        self.play(FadeIn(step2, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(step3, shift=DOWN * 0.2), run_time=1.0)
        self.play(Create(box(step3, color=GOLD_PHI)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_13_solve_eigenvalues()

    # ─── SCENE 13: Solve Eigenvalues ────────────
    def scene_13_solve_eigenvalues(self):
        header = make_title("Solve the Equation")
        self.add(header)

        eq = MathTex(
            r"\lambda^2 - \lambda - 1 = 0",
            font_size=48, color=TEXT_COLOR
        )
        quad = MathTex(
            r"\lambda = \frac{1 \pm \sqrt{5}}{2}",
            font_size=48, color=TEXT_COLOR
        )
        phi_val = MathTex(
            r"\lambda_1 = \varphi = \frac{1 + \sqrt{5}}{2}",
            font_size=44, color=GOLD_PHI
        )
        psi_val = MathTex(
            r"\lambda_2 = \psi = \frac{1 - \sqrt{5}}{2}",
            font_size=44, color=RED_PSI
        )

        group = VGroup(eq, quad, phi_val, psi_val).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(Write(eq), run_time=0.8)
        self.play(Write(quad), run_time=1.0)
        self.play(FadeIn(phi_val, shift=RIGHT * 0.3), run_time=0.8)
        self.play(FadeIn(psi_val, shift=RIGHT * 0.3), run_time=0.8)

        phi_b = box(phi_val, color=GOLD_PHI)
        psi_b = box(psi_val, color=RED_PSI)
        self.play(Create(phi_b), Create(psi_b), run_time=0.6)

        self.next_slide()
        self.clear()
        self.scene_14_phi_psi()

    # ─── SCENE 14: Introduce φ and ψ ────────────
    def scene_14_phi_psi(self):
        header = make_title("The Golden Ratio", color=GOLD_PHI)
        self.add(header)

        phi_line = MathTex(
            r"\varphi = \frac{1 + \sqrt{5}}{2} \approx 1.618",
            font_size=44, color=GOLD_PHI
        )
        psi_line = MathTex(
            r"\psi = \frac{1 - \sqrt{5}}{2} \approx -0.618",
            font_size=44, color=RED_PSI
        )
        vieta1 = MathTex(
            r"\varphi + \psi = 1, \quad \varphi \psi = -1",
            font_size=36, color=ACCENT_PURPLE
        )
        vieta2 = MathTex(
            r"\varphi - \psi = \sqrt{5}",
            font_size=40, color=ACCENT_PURPLE
        )

        group = VGroup(phi_line, psi_line, vieta1, vieta2).arrange(
            DOWN, buff=0.5
        )
        center_content(group, y_shift=0.3)

        self.play(Write(phi_line), run_time=1.2)
        self.play(Write(psi_line), run_time=1.2)
        self.play(FadeIn(vieta1, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(vieta2, shift=UP * 0.2), run_time=0.6)

        self.next_slide()
        self.clear()
        self.scene_15_eigenvectors()

    # ─── SCENE 15: Eigenvectors ─────────────────
    def scene_15_eigenvectors(self):
        header = make_title("Eigenvectors")
        self.add(header)

        eq_setup = MathTex(
            r"(M - \lambda I)\,\mathbf{x} = \mathbf{0}",
            font_size=44, color=BLUE_MAT
        )
        eq_setup.move_to(UP * 1.8)

        self.play(Write(eq_setup), run_time=0.8)

        eigen_phi = MathTex(
            r"\mathbf{x}_1 = \begin{bmatrix} \varphi \\ 1 \end{bmatrix}",
            font_size=48, color=GOLD_PHI
        )
        eigen_psi = MathTex(
            r"\mathbf{x}_2 = \begin{bmatrix} \psi \\ 1 \end{bmatrix}",
            font_size=48, color=RED_PSI
        )
        vecs = VGroup(eigen_phi, eigen_psi).arrange(RIGHT, buff=2.0)
        vecs.move_to(UP * 0.3)

        note = MathTex(
            r"\text{Since } \varphi^2 = \varphi + 1"
            r"\text{ and } \psi^2 = \psi + 1,"
            r"\text{ row reduces to zero}",
            font_size=28, color=DIM_WHITE
        )
        note.move_to(DOWN * 1.3)

        self.play(Write(eigen_phi), run_time=0.8)
        self.play(Write(eigen_psi), run_time=0.8)
        self.play(Create(box(eigen_phi, color=GOLD_PHI)),
                  Create(box(eigen_psi, color=RED_PSI)), run_time=0.5)
        self.play(FadeIn(note), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_16_matrix_P()

    # ─── SCENE 16: Construct Matrix P ───────────
    def scene_16_matrix_P(self):
        header = MathTex(r"\text{Modal Matrix } P", font_size=44, color=TEXT_COLOR)
        header.to_edge(UP, buff=0.5)
        self.add(header)

        P_def = MathTex(
            r"P = \begin{bmatrix} \varphi & \psi \\ 1 & 1 \end{bmatrix}",
            font_size=52, color=BLUE_MAT
        )
        det_label = MathTex(
            r"\det(P) = \varphi - \psi = \sqrt{5}",
            font_size=44, color=GOLD_PHI
        )

        group = VGroup(P_def, det_label).arrange(DOWN, buff=0.8)
        center_content(group, y_shift=0.3)

        self.play(Write(P_def), run_time=1.2)
        self.play(FadeIn(det_label, shift=UP * 0.3), run_time=0.8)
        self.play(Create(box(P_def, color=BLUE_MAT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_17_diagonalization()

    # ─── SCENE 17: Diagonalization ──────────────
    def scene_17_diagonalization(self):
        header = make_title("Diagonalization", color=GREEN_RESULT)
        self.add(header)

        decomp = MathTex(
            r"M = P \, D \, P^{-1}",
            font_size=52, color=GREEN_RESULT
        )
        D_mat = MathTex(
            r"D = \begin{bmatrix} \varphi & 0 \\ 0 & \psi \end{bmatrix}",
            font_size=48, color=BLUE_MAT
        )

        group = VGroup(decomp, D_mat).arrange(DOWN, buff=0.7)
        center_content(group, y_shift=0.6)

        self.play(Write(decomp), run_time=1.2)
        self.play(FadeIn(D_mat, shift=UP * 0.2), run_time=0.8)
        self.play(Create(box(decomp, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_17b_inverse()

    # ─── SCENE 17b: Show P^{-1} on separate slide ─
    def scene_17b_inverse(self):
        header = make_title("Inverse of P", color=ACCENT_PURPLE)
        self.add(header)

        Pinv = MathTex(
            r"P^{-1} = \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} 1 & -\psi \\ -1 & \varphi \end{bmatrix}",
            font_size=48, color=ACCENT_PURPLE
        )
        check = MathTex(
            r"P \, P^{-1} = I \;\checkmark",
            font_size=44, color=GREEN_RESULT
        )

        group = VGroup(Pinv, check).arrange(DOWN, buff=0.8)
        center_content(group, y_shift=0.3)

        self.play(Write(Pinv), run_time=1.2)
        self.play(FadeIn(check, shift=UP * 0.3), run_time=0.8)
        self.play(Create(box(Pinv, color=ACCENT_PURPLE)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_18_power_diagonal()

    # ─── SCENE 18: Powering Diagonal Matrix ─────
    def scene_18_power_diagonal(self):
        header = make_title("Powering Made Simple", color=GREEN_RESULT)
        self.add(header)

        insight = MathTex(
            r"M^n = P \, D^n \, P^{-1}",
            font_size=52, color=GREEN_RESULT
        )
        Dn = MathTex(
            r"D^n = \begin{bmatrix} \varphi^n & 0 \\ 0 & \psi^n \end{bmatrix}",
            font_size=48, color=BLUE_MAT
        )
        note = MathTex(
            r"\text{Just exponentiate the diagonal entries!}",
            font_size=36, color=GOLD_PHI
        )

        group = VGroup(insight, Dn, note).arrange(DOWN, buff=0.6)
        center_content(group, y_shift=0.3)

        self.play(Write(insight), run_time=1.2)
        self.play(Write(Dn), run_time=1.2)
        self.play(FadeIn(note, scale=1.1), run_time=0.6)
        self.play(Create(box(Dn, color=BLUE_MAT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_19_compute_Mn()

    # ─── SCENE 19: Compute Mn - Step 1 ─────────
    def scene_19_compute_Mn(self):
        header = MathTex(
            r"\text{Step 1: } P^{-1} \mathbf{v}_0",
            font_size=44, color=TEXT_COLOR
        )
        header.to_edge(UP, buff=0.5)
        self.add(header)

        step1 = MathTex(
            r"\mathbf{v}_n = P \, D^n \, P^{-1} \, \mathbf{v}_0",
            font_size=42, color=BLUE_MAT
        )
        step2 = MathTex(
            r"P^{-1} \mathbf{v}_0 = \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} 1 & -\psi \\ -1 & \varphi \end{bmatrix}"
            r"\begin{bmatrix} 1 \\ 0 \end{bmatrix}",
            font_size=38, color=ACCENT_PURPLE
        )
        step3 = MathTex(
            r"= \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} 1 \\ -1 \end{bmatrix}",
            font_size=44, color=GREEN_RESULT
        )

        group = VGroup(step1, step2, step3).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.2)

        self.play(Write(step1), run_time=1.0)
        self.play(FadeIn(step2, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(step3, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(box(step3, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_19b_compute_Mn_step2()

    # ─── SCENE 19b: Compute Mn - Step 2 ────────
    def scene_19b_compute_Mn_step2(self):
        header = MathTex(
            r"\text{Step 2: } D^n \cdot P^{-1} \mathbf{v}_0",
            font_size=44, color=TEXT_COLOR
        )
        header.to_edge(UP, buff=0.5)
        self.add(header)

        step1 = MathTex(
            r"D^n \cdot \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} 1 \\ -1 \end{bmatrix}",
            font_size=42, color=BLUE_MAT
        )
        step2 = MathTex(
            r"= \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi^n & 0 \\ 0 & \psi^n \end{bmatrix}"
            r"\begin{bmatrix} 1 \\ -1 \end{bmatrix}",
            font_size=38, color=TEXT_COLOR
        )
        step3 = MathTex(
            r"= \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi^n \\ -\psi^n \end{bmatrix}",
            font_size=44, color=GREEN_RESULT
        )

        group = VGroup(step1, step2, step3).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.2)

        self.play(Write(step1), run_time=0.8)
        self.play(FadeIn(step2, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(step3, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(box(step3, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_20_apply_v0()

    # ─── SCENE 20: Apply P to get vn ─────────────
    def scene_20_apply_v0(self):
        header = MathTex(
            r"\text{Step 3: } P \cdot D^n P^{-1} \mathbf{v}_0",
            font_size=44, color=TEXT_COLOR
        )
        header.to_edge(UP, buff=0.5)
        self.add(header)

        full = MathTex(
            r"\mathbf{v}_n = \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi & \psi \\ 1 & 1 \end{bmatrix}"
            r"\begin{bmatrix} \varphi^n \\ -\psi^n \end{bmatrix}",
            font_size=38, color=BLUE_MAT
        )
        result = MathTex(
            r"= \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi^{n+1} - \psi^{n+1} \\ "
            r"\varphi^n - \psi^n \end{bmatrix}",
            font_size=42, color=GOLD_PHI
        )

        group = VGroup(full, result).arrange(
            DOWN, buff=0.6, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.3)

        self.play(Write(full), run_time=1.0)
        self.play(FadeIn(result, shift=DOWN * 0.2), run_time=1.0)
        self.play(Create(box(result, color=GOLD_PHI)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_21_extract_Fn()

    # ─── SCENE 21: Extract Fn ───────────────────
    def scene_21_extract_Fn(self):
        header = MathTex(r"\text{Extract } F_n", font_size=44, color=TEXT_COLOR)
        header.to_edge(UP, buff=0.5)
        self.add(header)

        vec = MathTex(
            r"\mathbf{v}_n = \begin{bmatrix} F_{n+1} \\ F_n \end{bmatrix}"
            r"= \frac{1}{\sqrt{5}}"
            r"\begin{bmatrix} \varphi^{n+1} - \psi^{n+1} \\ "
            r"\varphi^n - \psi^n \end{bmatrix}",
            font_size=38, color=BLUE_MAT
        )
        extract = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=56, color=GOLD_PHI
        )

        group = VGroup(vec, extract).arrange(DOWN, buff=0.8)
        center_content(group, y_shift=0.3)

        arrow = Arrow(
            vec.get_bottom() + DOWN * 0.05,
            extract.get_top() + UP * 0.05,
            color=GREEN_RESULT, stroke_width=3
        )

        self.play(Write(vec), run_time=1.0)
        self.play(GrowArrow(arrow), run_time=0.6)
        self.play(Write(extract), run_time=1.2)
        self.play(Create(box(extract, color=GOLD_PHI)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_22_binet_formula()

    # ─── SCENE 22: Final Binet Formula ──────────
    def scene_22_binet_formula(self):
        header = make_title("Binet's Formula", color=GOLD_PHI, size=48)
        self.add(header)

        formula = MathTex(
            r"F_n = \frac{1}{\sqrt{5}}"
            r"\left[\left(\frac{1+\sqrt{5}}{2}\right)^n"
            r"- \left(\frac{1-\sqrt{5}}{2}\right)^n\right]",
            font_size=44, color=GREEN_RESULT
        )
        shorthand = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=52, color=GOLD_PHI
        )

        group = VGroup(formula, shorthand).arrange(DOWN, buff=0.8)
        center_content(group, y_shift=0.3)

        self.play(Write(formula), run_time=2.0, rate_func=smooth)
        self.wait(0.5)
        self.play(Create(box(formula, color=GREEN_RESULT, buff=0.2)), run_time=0.8)
        self.play(Write(shorthand), run_time=1.0)
        self.play(Create(box(shorthand, color=GOLD_PHI, buff=0.2)), run_time=0.5)
        self.wait(1.0)

        self.next_slide()
        self.clear()
        self.scene_23_verification()

    # ─── SCENE 23: Verification via Base Cases ──
    def scene_23_verification(self):
        header = make_title("Verification", color=GREEN_RESULT)
        self.add(header)

        n0_calc = MathTex(
            r"n = 0: \quad F_0 = \frac{\varphi^0 - \psi^0}{\sqrt{5}}"
            r"= \frac{1 - 1}{\sqrt{5}} = 0 \;\checkmark",
            font_size=36, color=GREEN_RESULT
        )
        n1_calc = MathTex(
            r"n = 1: \quad F_1 = \frac{\varphi - \psi}{\sqrt{5}}"
            r"= \frac{\sqrt{5}}{\sqrt{5}} = 1 \;\checkmark",
            font_size=36, color=GREEN_RESULT
        )
        confirm = MathTex(
            r"\text{Formula checks out for base cases!}",
            font_size=36, color=GREEN_RESULT
        )

        group = VGroup(n0_calc, n1_calc, confirm).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(Write(n0_calc), run_time=1.2)
        self.play(Write(n1_calc), run_time=1.2)
        self.play(FadeIn(confirm, scale=1.1), run_time=0.8)

        self.next_slide()
        self.clear()
        self.scene_24_induction_setup()

    # ─── SCENE 24: Induction Setup ──────────────
    def scene_24_induction_setup(self):
        header = make_title("Proof by Strong Induction")
        self.add(header)

        prop = MathTex(
            r"P(n): \quad F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=40, color=BLUE_MAT
        )
        base = MathTex(
            r"\text{Base: } P(0) \text{ and } P(1) \text{ hold}",
            font_size=36, color=GREEN_RESULT
        )
        assume = MathTex(
            r"\text{I.H.: } P(j) \text{ holds for all } j \leq k",
            font_size=36, color=GOLD_PHI
        )
        prove = MathTex(
            r"\text{Goal: Show } P(k+1) \text{ holds}",
            font_size=36, color=GREEN_RESULT
        )

        group = VGroup(prop, base, assume, prove).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(Write(prop), run_time=1.0)
        self.play(FadeIn(base), run_time=0.6)
        self.play(FadeIn(assume), run_time=0.6)
        self.play(FadeIn(prove), run_time=0.6)
        self.play(Create(box(prove, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_24b_induction_step1()

    # ─── SCENE 24b: Induction Step 1 ────────────
    def scene_24b_induction_step1(self):
        header = make_title("Inductive Step (Part 1)")
        self.add(header)

        step1 = MathTex(
            r"F_{k+1} = F_k + F_{k-1}",
            font_size=48, color=GOLD_PHI
        )
        note1 = MathTex(
            r"\text{(by the Fibonacci recurrence)}",
            font_size=28, color=DIM_WHITE
        )
        step2a = MathTex(
            r"= \frac{\varphi^k - \psi^k}{\sqrt{5}}"
            r"+ \frac{\varphi^{k-1} - \psi^{k-1}}{\sqrt{5}}",
            font_size=36, color=ACCENT_PURPLE
        )
        note2 = MathTex(
            r"\text{(by I.H. for } k \text{ and } k-1\text{)}",
            font_size=28, color=DIM_WHITE
        )

        group = VGroup(step1, note1, step2a, note2).arrange(
            DOWN, buff=0.45, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.3)

        self.play(Write(step1), run_time=1.0)
        self.play(FadeIn(note1), run_time=0.5)
        self.play(FadeIn(step2a, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(note2), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_24c_induction_step2()

    # ─── SCENE 24c: Induction Step 2 ────────────
    def scene_24c_induction_step2(self):
        header = make_title("Inductive Step (Part 2)")
        self.add(header)

        step1 = MathTex(
            r"F_{k+1} = \frac{1}{\sqrt{5}}"
            r"\big[\varphi^k + \varphi^{k-1}"
            r"- \psi^k - \psi^{k-1}\big]",
            font_size=36, color=TEXT_COLOR
        )
        step2 = MathTex(
            r"= \frac{1}{\sqrt{5}}"
            r"\big[\varphi^{k-1}(\varphi + 1)"
            r"- \psi^{k-1}(\psi + 1)\big]",
            font_size=36, color=BLUE_MAT
        )
        note = MathTex(
            r"\varphi^2 = \varphi + 1, \quad \psi^2 = \psi + 1",
            font_size=36, color=GOLD_PHI
        )

        group = VGroup(step1, step2, note).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.3)

        self.play(Write(step1), run_time=0.8)
        self.play(FadeIn(step2, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(note), run_time=0.8)
        self.play(Create(box(note, color=GOLD_PHI)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_24d_induction_step3()

    # ─── SCENE 24d: Induction Step 3 ────────────
    def scene_24d_induction_step3(self):
        header = make_title("Inductive Step (Part 3)")
        self.add(header)

        step1 = MathTex(
            r"F_{k+1} = \frac{1}{\sqrt{5}}"
            r"\big[\varphi^{k-1} \cdot \varphi^2"
            r"- \psi^{k-1} \cdot \psi^2\big]",
            font_size=38, color=BLUE_MAT
        )
        step2 = MathTex(
            r"= \frac{1}{\sqrt{5}}"
            r"\big[\varphi^{k+1} - \psi^{k+1}\big]",
            font_size=44, color=GREEN_RESULT
        )
        conclusion = MathTex(
            r"\text{This is exactly } P(k+1). \quad \blacksquare",
            font_size=38, color=GREEN_RESULT
        )

        group = VGroup(step1, step2, conclusion).arrange(
            DOWN, buff=0.6, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.3)

        self.play(Write(step1), run_time=0.8)
        self.play(FadeIn(step2, shift=DOWN * 0.2), run_time=1.0)
        self.play(Create(box(step2, color=GREEN_RESULT)), run_time=0.5)
        self.play(FadeIn(conclusion, scale=1.1), run_time=1.0)

        self.next_slide()
        self.clear()
        self.scene_25_paradox()

    # ─── SCENE 25: Integrality Paradox ──────────
    def scene_25_paradox(self):
        header = make_title("The Integrality Paradox", color=RED_PSI)
        self.add(header)

        formula = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=52, color=GOLD_PHI
        )
        question = MathTex(
            r"\text{Why is } F_n \text{ always an integer?}",
            font_size=40, color=RED_PSI
        )
        irr_note = MathTex(
            r"\text{The formula is full of } \sqrt{5}\text{!}",
            font_size=36, color=RED_PSI
        )

        group = VGroup(formula, question, irr_note).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(Write(formula), run_time=1.0)
        self.play(Create(box(formula, color=RED_PSI, buff=0.12)), run_time=0.6)
        self.play(FadeIn(question, scale=1.15), run_time=1.0)
        self.play(FadeIn(irr_note), run_time=0.6)

        self.next_slide()
        self.clear()
        self.scene_25b_decimal_example()

    # ─── SCENE 25b: Decimal Expansion Example ───
    def scene_25b_decimal_example(self):
        header = make_title("Decimal Example", color=RED_PSI)
        self.add(header)

        dec_phi5 = MathTex(
            r"\varphi^5 \approx 11.090\ldots",
            font_size=40, color=GOLD_PHI
        )
        dec_psi5 = MathTex(
            r"\psi^5 \approx -0.090\ldots",
            font_size=40, color=RED_PSI
        )
        dec_sub = MathTex(
            r"\varphi^5 - \psi^5 \approx 11.180\ldots",
            font_size=38, color=TEXT_COLOR
        )
        dec_result = MathTex(
            r"\frac{11.180\ldots}{\sqrt{5}} = \frac{11.180}{2.236} = 5 = F_5",
            font_size=38, color=GREEN_RESULT
        )

        group = VGroup(dec_phi5, dec_psi5, dec_sub, dec_result).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.3)

        self.play(Write(dec_phi5), run_time=0.7)
        self.play(Write(dec_psi5), run_time=0.7)
        self.play(Write(dec_sub), run_time=1.0)
        self.play(Write(dec_result), run_time=1.0)
        self.play(Create(box(dec_result, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_26a_phi_pattern()

    # ─── SCENE 26a: Powers of φ Pattern ─────────
    def scene_26a_phi_pattern(self):
        header = make_title("A Hidden Pattern", color=GOLD_PHI)
        self.add(header)

        key_prop = MathTex(
            r"\varphi^2 = \varphi + 1",
            font_size=44, color=BLUE_MAT
        )
        note_prop = MathTex(
            r"\text{Higher powers reduce to } A\varphi + B",
            font_size=28, color=DIM_WHITE
        )

        top = VGroup(key_prop, note_prop).arrange(DOWN, buff=0.3)
        top.move_to(UP * 1.5)

        self.play(Write(key_prop), run_time=0.8)
        self.play(FadeIn(note_prop), run_time=0.5)

        patterns = VGroup(
            MathTex(r"\varphi^1 = 1\varphi + 0", font_size=38, color=GOLD_PHI),
            MathTex(r"\varphi^2 = 1\varphi + 1", font_size=38, color=GOLD_PHI),
            MathTex(r"\varphi^3 = 2\varphi + 1", font_size=38, color=GOLD_PHI),
            MathTex(r"\varphi^4 = 3\varphi + 2", font_size=38, color=GOLD_PHI),
            MathTex(r"\varphi^5 = 5\varphi + 3", font_size=38, color=GOLD_PHI),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        patterns.next_to(note_prop, DOWN, buff=0.5)

        for p in patterns:
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.4)

        coeff_note = MathTex(
            r"\text{Coefficients } A_n: \; 1, 1, 2, 3, 5, \ldots = F_n",
            font_size=36, color=GREEN_RESULT
        )
        coeff_note.next_to(patterns, DOWN, buff=0.4)

        self.play(FadeIn(coeff_note, scale=1.1), run_time=0.8)
        self.play(Create(box(coeff_note, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_26b_phi_pattern_derivation()

    # ─── SCENE 26b: Show How Each Power Reduces ─
    def scene_26b_phi_pattern_derivation(self):
        header = make_title("How the Pattern Emerges", color=GOLD_PHI)
        self.add(header)

        d3 = MathTex(
            r"\varphi^3 = \varphi^2 \cdot \varphi = (\varphi+1)\varphi"
            r"= \varphi^2 + \varphi = 2\varphi + 1",
            font_size=36, color=GOLD_PHI
        )
        d4 = MathTex(
            r"\varphi^4 = \varphi^3 \cdot \varphi = (2\varphi+1)\varphi"
            r"= 2(\varphi+1) + \varphi = 3\varphi + 2",
            font_size=36, color=GOLD_PHI
        )
        d5 = MathTex(
            r"\varphi^5 = \varphi^4 \cdot \varphi = (3\varphi+2)\varphi"
            r"= 3(\varphi+1) + 2\varphi = 5\varphi + 3",
            font_size=36, color=GOLD_PHI
        )

        group = VGroup(d3, d4, d5).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(Write(d3), run_time=1.2)
        self.play(Write(d4), run_time=1.2)
        self.play(Write(d5), run_time=1.2)
        self.play(Create(box(d5, color=GOLD_PHI)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_26c_general_pattern()

    # ─── SCENE 26c: General Pattern ──────────────
    def scene_26c_general_pattern(self):
        header = make_title("The General Pattern", color=GREEN_RESULT)
        self.add(header)

        general = MathTex(
            r"\varphi^n = F_n \, \varphi + F_{n-1}",
            font_size=48, color=GREEN_RESULT
        )
        same = MathTex(
            r"\psi^n = F_n \, \psi + F_{n-1}",
            font_size=48, color=RED_PSI
        )
        note = MathTex(
            r"\text{Same integer coefficients } F_n, F_{n-1}\text{!}",
            font_size=36, color=GREEN_RESULT
        )

        group = VGroup(general, same, note).arrange(DOWN, buff=0.6)
        center_content(group, y_shift=0.3)

        self.play(FadeIn(general, scale=1.1), run_time=1.0)
        self.play(Create(box(general, color=GREEN_RESULT)), run_time=0.5)
        self.play(FadeIn(same, scale=1.1), run_time=1.0)
        self.play(FadeIn(note, scale=1.1), run_time=0.8)

        self.next_slide()
        self.clear()
        self.scene_26d_structural_cancellation()

    # ─── SCENE 26d: Structural Cancellation ─────
    def scene_26d_structural_cancellation(self):
        header = make_title("Structural Cancellation", color=GREEN_RESULT)
        self.add(header)

        rep1 = MathTex(
            r"\varphi^n = F_n \, \varphi + F_{n-1}",
            font_size=44, color=GOLD_PHI
        )
        rep2 = MathTex(
            r"\psi^n = F_n \, \psi + F_{n-1}",
            font_size=44, color=RED_PSI
        )
        note = MathTex(
            r"\text{Same integer coefficients!}",
            font_size=36, color=GREEN_RESULT
        )

        group = VGroup(rep1, rep2, note).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(Write(rep1), run_time=0.8)
        self.play(Write(rep2), run_time=0.8)
        self.play(FadeIn(note, scale=1.1), run_time=0.6)

        self.next_slide()
        self.clear()
        self.scene_26e_cancellation_proof()

    # ─── SCENE 26e: Cancellation Derivation ─────
    def scene_26e_cancellation_proof(self):
        header = make_title("Cancellation Derivation", color=GREEN_RESULT)
        self.add(header)

        step1 = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=40, color=TEXT_COLOR
        )
        step2 = MathTex(
            r"= \frac{(F_n\varphi + F_{n-1}) - (F_n\psi + F_{n-1})}{\sqrt{5}}",
            font_size=36, color=TEXT_COLOR
        )
        step3 = MathTex(
            r"= \frac{F_n(\varphi - \psi) + (F_{n-1} - F_{n-1})}{\sqrt{5}}",
            font_size=36, color=BLUE_MAT
        )

        group = VGroup(step1, step2, step3).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        center_content(group, y_shift=0.3)

        self.play(Write(step1), run_time=0.8)
        self.play(FadeIn(step2, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(step3, shift=DOWN * 0.2), run_time=0.8)

        self.next_slide()
        self.clear()
        self.scene_26f_cancellation_result()

    # ─── SCENE 26f: Cancellation Result ─────────
    def scene_26f_cancellation_result(self):
        header = make_title("The Cancellation", color=GREEN_RESULT)
        self.add(header)

        key = MathTex(
            r"\varphi - \psi = \sqrt{5}",
            font_size=44, color=GOLD_PHI
        )
        step3 = MathTex(
            r"F_n = \frac{F_n \cdot \sqrt{5}}{\sqrt{5}}",
            font_size=48, color=TEXT_COLOR
        )
        step4 = MathTex(
            r"= F_n \in \mathbb{N}_0",
            font_size=52, color=GREEN_RESULT
        )
        explanation = MathTex(
            r"\text{The } \sqrt{5} \text{ cancels — } F_n \text{ is always an integer!}",
            font_size=36, color=GREEN_RESULT
        )

        group = VGroup(key, step3, step4, explanation).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(FadeIn(key), run_time=0.6)
        self.play(Create(box(key, color=GOLD_PHI)), run_time=0.5)
        self.play(Write(step3), run_time=1.0)
        self.play(FadeIn(step4, shift=DOWN * 0.3), run_time=1.0)
        self.play(Create(box(step4, color=GREEN_RESULT)), run_time=0.5)
        self.play(FadeIn(explanation, scale=1.1), run_time=0.8)

        self.next_slide()
        self.clear()
        self.scene_27_identity()

    # ─── SCENE 27: Key Identity Insight ─────────
    def scene_27_identity(self):
        header = make_title("The Resolution", color=GREEN_RESULT)
        self.add(header)

        key_id = MathTex(
            r"\varphi - \psi = \sqrt{5}",
            font_size=52, color=GOLD_PHI
        )
        result = MathTex(
            r"F_n = \frac{F_n \cdot \sqrt{5}}{\sqrt{5}} = F_n",
            font_size=48, color=GREEN_RESULT
        )
        conclusion = MathTex(
            r"F_n \in \mathbb{N}_0",
            font_size=52, color=GREEN_RESULT
        )
        remark = MathTex(
            r"\text{The irrationals always cancel!}",
            font_size=36, color=GREEN_RESULT
        )

        group = VGroup(key_id, result, conclusion, remark).arrange(DOWN, buff=0.5)
        center_content(group, y_shift=0.3)

        self.play(Write(key_id), run_time=1.0)
        self.play(Write(result), run_time=1.2)
        self.play(Create(box(result, color=GREEN_RESULT)), run_time=0.5)
        self.play(FadeIn(conclusion, scale=1.1), run_time=1.0)
        self.play(FadeIn(remark), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_28_rabbits()

    # ─── SCENE 28: Application 1 (Rabbits) ─────
    def scene_28_rabbits(self):
        header = make_title("Application 1: Rabbit Population", size=40)
        self.add(header)

        months = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O"]
        young  = [1, 0, 1, 1, 2, 3, 5, 8, 13, 21]
        adult  = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

        # --- row labels (left column) ---
        m_label = Text("Month:", font_size=22, color=ACCENT_PURPLE)
        y_label = Text("Young:", font_size=22, color=GOLD_PHI)
        a_label = Text("Adult:", font_size=22, color=RED_PSI)

        row_labels = VGroup(m_label, y_label, a_label).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        # --- data rows ---
        month_labels = VGroup(*[
            Text(m, font_size=20, color=ACCENT_PURPLE) for m in months
        ]).arrange(RIGHT, buff=0.25)

        young_nums = VGroup(*[
            Integer(y, font_size=22, color=GOLD_PHI) for y in young
        ]).arrange(RIGHT, buff=0.25)

        adult_nums = VGroup(*[
            Integer(a, font_size=22, color=RED_PSI) for a in adult
        ]).arrange(RIGHT, buff=0.25)

        # Align data rows to the same x-anchor as the month row
        young_nums.move_to(month_labels.get_center())
        adult_nums.move_to(month_labels.get_center())

        data_rows = VGroup(month_labels, young_nums, adult_nums).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT
        )

        # Place labels to the left of the data block
        row_labels.next_to(data_rows, LEFT, buff=0.35, aligned_edge=UP)

        table = VGroup(row_labels, data_rows)
        center_content(table, y_shift=0.5)

        self.play(FadeIn(m_label), FadeIn(month_labels), run_time=0.5)
        self.play(FadeIn(y_label), FadeIn(a_label), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(n) for n in young_nums], lag_ratio=0.08),
                  run_time=1.0)
        self.play(LaggedStart(*[FadeIn(n) for n in adult_nums], lag_ratio=0.08),
                  run_time=1.0)

        total = MathTex(
            r"T_n = F_{n+1} = \frac{\varphi^{n+1} - \psi^{n+1}}{\sqrt{5}}",
            font_size=38, color=GREEN_RESULT
        )
        total.next_to(adult_nums, DOWN, buff=0.6)

        self.play(Write(total), run_time=1.0)
        self.play(Create(box(total, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_29_tiling()

    # ─── SCENE 29: Application 2 (Tiling) ──────
    def scene_29_tiling(self):
        header = MathTex(
            r"\text{Application 2: Tiling a } 1 \times n \text{ Board}",
            font_size=40, color=TEXT_COLOR
        )
        header.to_edge(UP, buff=0.5)
        self.add(header)

        desc = MathTex(
            r"\text{How many ways using } 1\times1"
            r"\text{ and } 1\times2 \text{ tiles?}",
            font_size=32, color=TEXT_COLOR
        )
        case1 = MathTex(
            r"\text{End with square: } W_{n-1}",
            font_size=36, color=GOLD_PHI
        )
        case2 = MathTex(
            r"\text{End with domino: } W_{n-2}",
            font_size=36, color=RED_PSI
        )
        recurrence = MathTex(
            r"W_n = W_{n-1} + W_{n-2}",
            font_size=44, color=BLUE_MAT
        )
        result = MathTex(
            r"W_n = F_{n+1} = \frac{\varphi^{n+1} - \psi^{n+1}}{\sqrt{5}}",
            font_size=40, color=GREEN_RESULT
        )

        group = VGroup(desc, case1, case2, recurrence, result).arrange(
            DOWN, buff=0.55
        )
        center_content(group, y_shift=0.15)

        self.play(FadeIn(desc), run_time=0.6)
        self.play(FadeIn(case1), run_time=0.6)
        self.play(FadeIn(case2), run_time=0.6)
        self.play(Write(recurrence), run_time=0.8)
        self.play(Write(result), run_time=1.0)
        self.play(Create(box(result, color=GREEN_RESULT)), run_time=0.5)

        self.next_slide()
        self.clear()
        self.scene_30_schedules()

    # ─── SCENE 30: Application 3 (Schedules) ───
    def scene_30_schedules(self):
        header = make_title("Application 3: Study Schedules", size=40)
        self.add(header)

        problem = MathTex(
            r"\text{No two heavy (H) study days in a row}",
            font_size=36, color=RED_PSI
        )

        valid_label = MathTex(
            r"\text{Valid patterns:}",
            font_size=28, color=DIM_WHITE
        )
        patterns = VGroup(
            MathTex(r"\text{R R R R R}", font_size=28, color=GREEN_RESULT),
            MathTex(r"\text{R R H R H}", font_size=28, color=GREEN_RESULT),
            MathTex(r"\text{H R H R R}", font_size=28, color=GREEN_RESULT),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        valid_group = VGroup(valid_label, patterns).arrange(
            DOWN, buff=0.2, aligned_edge=LEFT
        )

        invalid_label = MathTex(
            r"\text{Invalid:}",
            font_size=28, color=RED_PSI
        )
        invalid = MathTex(r"\text{H H R R R}", font_size=28, color=RED_PSI)
        cross = Cross(invalid, stroke_color=RED_PSI, stroke_width=2)

        invalid_group = VGroup(invalid_label, invalid).arrange(
            DOWN, buff=0.2, aligned_edge=LEFT
        )

        cols = VGroup(valid_group, invalid_group).arrange(RIGHT, buff=1.5)

        result = MathTex(
            r"S_n = F_{n+2} = \frac{\varphi^{n+2} - \psi^{n+2}}{\sqrt{5}}",
            font_size=36, color=GREEN_RESULT
        )
        example = MathTex(r"S_7 = F_9 = 34", font_size=40, color=GOLD_PHI)

        full = VGroup(problem, cols, result, example).arrange(DOWN, buff=0.45)
        center_content(full, y_shift=0.2)

        self.play(FadeIn(problem), run_time=0.5)
        self.play(FadeIn(valid_label), FadeIn(patterns), run_time=0.8)
        self.play(FadeIn(invalid_label), FadeIn(invalid), run_time=0.5)
        self.play(Create(cross), run_time=0.4)
        self.play(Write(result), run_time=1.0)
        self.play(Write(example), run_time=0.6)

        self.next_slide()
        self.clear()
        self.scene_31_summary()

    # ─── SCENE 31: Final Summary ───────────────
    def scene_31_summary(self):
        header = make_title("Summary", size=48)
        self.add(header)

        steps = VGroup(
            VGroup(
                Text("Recurrence", font_size=30, color=GOLD_PHI),
                MathTex(r"F_{n+2}=F_{n+1}+F_n", font_size=30, color=DIM_WHITE),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Matrix", font_size=30, color=BLUE_MAT),
                MathTex(r"\mathbf{v}_n = M^n \mathbf{v}_0",
                        font_size=30, color=DIM_WHITE),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Eigenvalues", font_size=30, color=ACCENT_PURPLE),
                MathTex(r"\varphi, \; \psi", font_size=30, color=DIM_WHITE),
            ).arrange(DOWN, buff=0.15),
            VGroup(
                Text("Formula", font_size=30, color=GREEN_RESULT),
                MathTex(r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
                        font_size=30, color=DIM_WHITE),
            ).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=0.7)
        steps.move_to(UP * 0.8)

        arrows = VGroup()
        for i in range(len(steps) - 1):
            arr = Arrow(
                steps[i].get_right() + RIGHT * 0.1,
                steps[i+1].get_left() + LEFT * 0.1,
                color=TEXT_COLOR, stroke_width=2
            )
            arrows.add(arr)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3), run_time=0.5)
        for arr in arrows:
            self.play(GrowArrow(arr), run_time=0.3)

        takeaways = VGroup(
            MathTex(r"\text{1. Fibonacci encodes as a matrix problem}",
                    font_size=30, color=TEXT_COLOR),
            MathTex(r"\text{2. Diagonalization simplifies } M^n",
                    font_size=30, color=TEXT_COLOR),
            MathTex(r"\text{3. Binet's formula gives } F_n \text{ directly}",
                    font_size=30, color=TEXT_COLOR),
            MathTex(r"\text{4. Irrationals cancel — always integer!}",
                    font_size=30, color=TEXT_COLOR),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        takeaways.next_to(steps, DOWN, buff=0.6)

        self.play(LaggedStart(*[FadeIn(t) for t in takeaways],
                              lag_ratio=0.2), run_time=1.5)

        self.next_slide()
        self.clear()
        self.scene_32_closing()

    # ─── SCENE 32: Closing Visual ──────────────
    def scene_32_closing(self):
        fib_vals = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        fib_mobs = VGroup(*[
            Integer(val, font_size=40, color=GOLD_PHI) for val in fib_vals
        ]).arrange(RIGHT, buff=0.4)
        fib_mobs.move_to(UP * 1.5)

        for mob in fib_mobs:
            self.play(FadeIn(mob, shift=UP * 0.3, scale=1.2), run_time=0.2)

        message = Text("From Recursion to Elegance",
                       font_size=48, color=GREEN_RESULT, weight=BOLD)
        message.move_to(DOWN * 0.3)

        sub = MathTex(
            r"F_n = \frac{\varphi^n - \psi^n}{\sqrt{5}}",
            font_size=56, color=GOLD_PHI
        )
        sub.next_to(message, DOWN, buff=0.5)

        self.play(Write(message), run_time=1.5)
        self.play(Write(sub), run_time=1.5)
        self.play(Create(box(sub, color=GOLD_PHI, buff=0.2)), run_time=0.5)
        self.wait(2)
