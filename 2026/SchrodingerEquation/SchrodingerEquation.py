from typing import override

from manim import *
from manim.typing import Vector3D

Text.set_default(font="LXGW WenKai")

# 巴尔末系数据 (波长nm, 标签, 颜色)
_balmer_data = [
    (656.3, r"H_\alpha"),
    (486.1, r"H_\beta"),
    (434.0, r"H_\gamma"),
    (410.2, r"H_\delta"),
]


def wl2rgb(wl: int, gamma: float = 0.8):
    if 380 <= wl <= 440:
        r = -(wl - 440) / (440 - 380)
        g = 0.0
        b = 1.0
    elif 440 <= wl <= 490:
        r = 0.0
        g = (wl - 440) / (490 - 440)
        b = 1.0
    elif 490 <= wl <= 510:
        r = 0.0
        g = 1.0
        b = -(wl - 510) / (510 - 490)
    elif 510 <= wl <= 580:
        r = (wl - 510) / (580 - 510)
        g = 1.0
        b = 0.0
    elif 580 <= wl <= 645:
        r = 1.0
        g = -(wl - 645) / (645 - 580)
        b = 0.0
    elif 645 <= wl <= 780:
        r = 1.0
        g = 0.0
        b = 0.0
    else:
        # 紫外 / 红外，无可见光，返回黑色
        return (0.0, 0.0, 0.0)

    # 边缘衰减：380–420nm、700–780nm亮度降低
    if 380 <= wl <= 420:
        factor = 0.3 + 0.7 * (wl - 380) / (420 - 380)
    elif 700 <= wl <= 780:
        factor = 0.3 + 0.7 * (780 - wl) / (780 - 700)
    else:
        factor = 1.0

    def adjust(val: float) -> float:
        if val <= 0:
            return 0.0
        return pow(val * factor, gamma)

    r = adjust(r)
    g = adjust(g)
    b = adjust(b)

    return int(255 * r), int(255 * g), int(255 * b)


def wl2color(wl: float, gamma: float = 0.8) -> ManimColor:
    """
    将可见光波长(nm)转为 RGB (0~1 浮点数)
    :param wavelength: 波长，单位 nm，有效区间 380 ~ 780
    :param gamma: 伽马校正
    :return: (r, g, b) 取值范围 [0, 1]
    """
    if 380 <= wl <= 440:
        r = -(wl - 440) / (440 - 380)
        g = 0.0
        b = 1.0
    elif 440 <= wl <= 490:
        r = 0.0
        g = (wl - 440) / (490 - 440)
        b = 1.0
    elif 490 <= wl <= 510:
        r = 0.0
        g = 1.0
        b = -(wl - 510) / (510 - 490)
    elif 510 <= wl <= 580:
        r = (wl - 510) / (580 - 510)
        g = 1.0
        b = 0.0
    elif 580 <= wl <= 645:
        r = 1.0
        g = -(wl - 645) / (645 - 580)
        b = 0.0
    elif 645 <= wl <= 780:
        r = 1.0
        g = 0.0
        b = 0.0
    else:
        # 紫外 / 红外，无可见光，返回黑色
        return BLACK

    # 边缘衰减：380–420nm、700–780nm亮度降低
    if 380 <= wl <= 420:
        factor = 0.3 + 0.7 * (wl - 380) / (420 - 380)
    elif 700 <= wl <= 780:
        factor = 0.3 + 0.7 * (780 - wl) / (780 - 700)
    else:
        factor = 1.0

    def adjust(val: float) -> float:
        if val <= 0:
            return 0.0
        return pow(val * factor, gamma)

    r = adjust(r)
    g = adjust(g)
    b = adjust(b)

    return ManimColor((r, g, b))


def sin_wl2color(sin_wl: float) -> ManimColor:
    """
    :sin_wl [PI / 5, PI * 2]
    """
    wl = (sin_wl - PI / 5) / (PI * 2 - PI / 5) * 300 + 400
    return wl2color(wl)


def get_spectrum(
    data: list[tuple[float, str]],
    title: str,
    spec_width: float = 10.0,
    spec_height: float = 1.8,
):
    wl_min = 360
    wl_max = 670

    def wl_to_x(wl: float):
        ratio = (wl_max - wl) / (wl_max - wl_min)
        return -spec_width / 2 + ratio * spec_width

    spectrum = VDict()

    spec_bg = Rectangle(
        width=spec_width,
        height=spec_height,
        fill_color=BLACK,
        stroke_color=GRAY,
        stroke_width=1,
    ).move_to(ORIGIN)

    spec_lines = VGroup()
    spec_labels = VGroup()
    for wl, tex in data:
        x = wl_to_x(wl)
        color = wl2color(wl)
        line = Line(
            (x, -spec_height / 2, 0),
            (x, spec_height / 2, 0),
            stroke_color=color,
            stroke_width=3,
        )
        spec_lines += line

        label = MathTex(tex, color=color).scale(0.7).next_to(line, DOWN)
        spec_labels += label

    spec_l_label = (
        Text("360 nm", font_size=24).next_to(spec_bg.get_corner(UL), UP).set_color(GRAY)
    )
    spec_r_label = (
        Text("670 nm", font_size=24).next_to(spec_bg.get_corner(UR), UP).set_color(GRAY)
    )
    spec_title = Text(title, font_size=24).next_to(spec_bg, UP).set_color(GRAY)
    spectrum.add(
        [
            ("bg", spec_bg),
            ("lines", spec_lines),
            ("labels", spec_labels),
            ("l_label", spec_l_label),
            ("r_label", spec_r_label),
            ("title", spec_title),
        ]
    )
    return spectrum


def get_image(name: str) -> ImageMobject:
    return ImageMobject(f".\\2026\\SchrodingerEquation\\imgs\\{name}.png")


def get_full_spectrum_data(
    width: int = 40, height: int = 120, wl_start: int = 380, wl_end: int = 780
):
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    wls = np.linspace(wl_start, wl_end, height)

    for h in range(height):
        r, g, b = wl2rgb(wls[h])
        img_array[h, :] = [r, g, b]
    return img_array


def get_full_spectrum():
    spec_data = get_full_spectrum_data()
    return ImageMobject(spec_data)


def display_all(P: dict[str, bool]):
    for i in P:
        P[i] = False


# preview contraler
_P = {
    "开场白": True,
    "视频目录": True,
    "概述": True,
    "微观粒子篇": True,
    "current": False,
    "后话": True,
}

# display_all(_P)


class SchrodingerEquation(Scene):
    @override
    def construct(self) -> None:
        # region
        self.next_section(skip_animations=_P["开场白"])

        xue_ding_e = Text("薛定谔方程").set_color_by_gradient(BLUE, LIGHT_PINK)
        xue_ding_e_eq = MathTex(
            "i",
            r"\hbar \frac{\partial \varPsi}{\partial t}",
            "=-",
            r"\frac{\hbar ^2}{2m}\frac{\partial ^2\varPsi}{\partial x^2}",
            "+",
            r"V\varPsi",
        ).scale(1.5)

        original_cde_eq = xue_ding_e_eq.copy()

        simplified_xde_eq = MathTex(r"C_1 f_t' = C_2 f_x '' +V f")

        i = xue_ding_e_eq[0]
        rest = xue_ding_e_eq[1:]
        self.play(Write(xue_ding_e))
        self.wait()
        self.play(xue_ding_e.animate.to_edge(UP), FadeIn(xue_ding_e_eq, shift=UP))
        self.wait()
        self.play(Transform(xue_ding_e_eq, simplified_xde_eq))
        self.wait()
        self.play(Transform(xue_ding_e_eq, original_cde_eq))
        i_rect = SurroundingRectangle(i)
        self.play(
            i.animate.set_color(PURE_YELLOW),
            Create(i_rect),
            rest.animate.set_color(GRAY),
        )
        self.wait()
        self.play(
            FadeOut(rest, xue_ding_e, i_rect),
            i.animate.move_to(ORIGIN).scale(2),
        )
        self.wait()

        self.play(
            Indicate(i),
        )

        def_of_i = MathTex("i^2", " = -1")
        def_of_i[0].set_color(PURE_YELLOW)
        self.wait()
        self.play(i.animate.scale(1 / 2))
        self.play(ReplacementTransform(i, def_of_i))
        self.wait(2)

        self.play(FadeOut(def_of_i))

        # endregion

        # ==============================================================================
        self.next_section(skip_animations=_P["视频目录"])

        content_title = (
            Text("Road Map")
            .set_color(LIGHT_PINK)
            .scale(1.1)
            .to_edge(UP, buff=MED_SMALL_BUFF)
        )
        spliter_1 = Line(LEFT * 5, RIGHT * 5).next_to(content_title, DOWN, 0.3)

        section_1 = Text("1. 微观粒子")
        section_2 = Text("2. 能量守恒")
        section_3 = Text("3. 波的方程")
        section_4 = Text("4. 引入虚数")

        content = VGroup(section_1, section_2, section_3, section_4).arrange(
            DOWN, buff=MED_SMALL_BUFF
        )
        subtitles = [sec[2:] for sec in content]

        self.play(
            Write(content_title),
            Create(spliter_1),
            FadeIn(content, lag_ratio=0.9),
            run_time=2,
        )
        self.wait()

        self.play(
            *[FadeOut(sec[:2], shift=LEFT) for sec in content],
            *[sec.animate.to_edge(LEFT).shift(UP * 0.5) for sec in subtitles],
        )

        subtitles_rect = SurroundingRectangle(
            *subtitles, color=GRAY, buff=MED_SMALL_BUFF, corner_radius=0.3
        )

        pip_rect_width = (
            config.frame_width + subtitles_rect.get_right()[0] - MED_SMALL_BUFF
        )
        pip_rect_height = (
            config.frame_y_radius + subtitles_rect.get_top()[1] - MED_SMALL_BUFF
        )
        pip_rect = (
            RoundedRectangle(width=pip_rect_width, height=pip_rect_height)
            .set_color(GRAY)
            .to_corner(DR, buff=MED_SMALL_BUFF)
        )

        self.play(Create(subtitles_rect), Create(pip_rect))

        self.wait()
        # ==============================================================================
        self.next_section(skip_animations=_P["概述"])
        self.play(
            subtitles[0].animate.scale(1.1).set_color(YELLOW),
            *[
                subtitles[i].animate.set_color(GRAY)
                for i in range(len(subtitles))
                if i != 0
            ],
        )
        self.wait()

        spectrum = (
            get_spectrum(_balmer_data, "巴尔末系")
            .next_to(pip_rect.get_top(), DOWN)
            .shift(LEFT)
            .scale(0.7)
        )
        balmer = get_image("balmer").scale_to_fit_height(2).next_to(spectrum, RIGHT)
        balmer_eq = (
            MathTex(r"\lambda = B \frac{n^2}{n^2-4}")
            .set_color(YELLOW)
            .next_to(spectrum, DOWN)
        )

        self.play(Create(spectrum), Write(balmer_eq), FadeIn(balmer))
        self.wait()

        self.play(FadeOut(spectrum, balmer_eq, balmer, shift=DOWN))
        debroglie = get_image("debroglie").scale_to_fit_height(2)
        einstein = get_image("einstein").scale_to_fit_height(2)
        two_core_eq = (
            MathTex(
                r"""
            \begin{cases}
            E = h \nu                         \\
            \displaystyle   p = {h \over \lambda}
            \end{cases}"""
            )
            .set_color(YELLOW)
            .next_to(pip_rect.get_top(), DOWN, MED_LARGE_BUFF)
            .scale(1.5)
        )
        debroglie.next_to(two_core_eq, LEFT, buff=LARGE_BUFF)
        einstein.next_to(two_core_eq, RIGHT, buff=LARGE_BUFF)

        self.play(Write(two_core_eq), FadeIn(debroglie, einstein))

        self.wait()

        self.play(FadeOut(two_core_eq, debroglie, einstein, shift=DOWN))

        # ==============================================================================
        self.play(
            subtitles[0].animate.scale(1 / 1.1).set_color(GRAY),
            subtitles[1].animate.scale(1.1).set_color(YELLOW),
        )
        self.wait()

        # ==============================================================================
        self.play(
            subtitles[1].animate.scale(1 / 1.1).set_color(GRAY),
            subtitles[2].animate.scale(1.1).set_color(YELLOW),
        )

        self.wait()

        # ==============================================================================
        self.play(
            subtitles[2].animate.scale(1 / 1.1).set_color(GRAY),
            subtitles[3].animate.scale(1.1).set_color(YELLOW),
        )
        self.wait()
        self.play(subtitles[3].animate.scale(1 / 1.1).set_color(GRAY))
        self.wait()

        # ==============================================================================
        self.next_section(skip_animations=_P["微观粒子篇"])

        self.play(
            Indicate(subtitles[0]),
            FadeOut(
                content_title,
                *[subtitles[i] for i in range(len(subtitles)) if i != 0],
                subtitles_rect,
                pip_rect,
            ),
        )
        subtitle_shift = subtitles[0].get_center()[0]
        self.play(
            subtitles[0]
            .animate.to_edge(UP, buff=MED_SMALL_BUFF)
            .shift(-subtitle_shift * RIGHT)
            .set_color(LIGHT_PINK),
        )
        self.wait()
        year = Integer(1853)
        self.play(FadeIn(year))
        self.play(year.animate.set_color(GRAY).to_corner(DR))
        anders = get_image("anders").to_edge(RIGHT)
        spectrum.move_to(ORIGIN).scale(1 / 0.9)
        self.play(FadeIn(anders))
        self.play(
            *[Create(spectrum[iter]) for iter in ["bg", "lines", "l_label", "r_label"]]
        )
        self.wait()
        self.play(FadeOut(anders))
        balmer.to_edge(RIGHT)
        self.play(
            year.animate.set_value(1885),
        )
        self.play(FadeIn(balmer))
        self.wait()
        balmer_eq.next_to(spectrum, DOWN)
        spectrum["title"].set_color(PURE_YELLOW)
        self.play(Create(spectrum["labels"]), Write(balmer_eq))
        self.play(Write(spectrum["title"]))
        self.wait()
        self.play(FadeOut(balmer))
        maxwell = get_image("maxwell").to_edge(LEFT)
        self.play(year.animate.set_value(1864), FadeOut(spectrum, balmer_eq))
        self.play(FadeIn(maxwell))
        annotation_1 = (
            Text("*该方程是简化版本，非Maxwell原版。", font_size=15)
            .to_edge(DOWN, buff=SMALL_BUFF)
            .set_color(GRAY)
        )
        maxwell_eqs = MathTex(r"""\begin{cases}
    \displaystyle \nabla \cdot \,\,\mathbf{E}
            =\frac{\rho _e}{\epsilon _0}              \\
	\displaystyle \nabla \times   \mathbf{E}
            =-\frac{\partial \mathbf{B}}{\partial t}  \\
	\displaystyle \nabla \cdot \,\,\mathbf{B}
            =0                                        \\
	\displaystyle \nabla \times   \mathbf{B}
            =\epsilon _0\mu _0\frac{\partial \mathbf{E}}{\partial t}+\mu _0\mathbf{j} \\
\end{cases}""")

        self.play(Write(maxwell_eqs), Write(annotation_1))

        self.wait()
        # wl的数值应该介于 [PI/5,PI*2]
        wl_0 = ValueTracker(PI / 5)
        phi_0 = ValueTracker(0)
        A_0 = 0.3
        t_range_0 = (0, 10)
        wave_0_shift = LEFT * 3
        wave_0 = ParametricFunction(
            lambda t: (t, A_0 * np.sin(2 * PI / wl_0.get_value() * t), 0),
            t_range=t_range_0,
            color=sin_wl2color(wl_0.get_value()),
        ).shift(wave_0_shift)

        self.play(FadeOut(maxwell_eqs, annotation_1), FadeIn(wave_0))

        def update_wave_0(mob: Mobject):
            return mob.become(
                ParametricFunction(
                    lambda t: (
                        t,
                        A_0 * np.sin(2 * PI / wl_0.get_value() * t + phi_0.get_value()),
                        0,
                    ),
                    t_range=t_range_0,
                    color=sin_wl2color(wl_0.get_value()),
                )
            ).shift(wave_0_shift)

        wave_0.add_updater(update_wave_0)
        self.play(wl_0.animate.set_value(2 * PI), run_time=4, rate_func=linear)
        self.play(wl_0.animate.set_value(PI), run_time=2, rate_func=linear)

        electronic_c1 = Circle(0.1).set_color(BLUE)
        electronic_c2 = Text("-").set_color(BLUE).scale(0.5)
        electron = (
            VGroup(electronic_c1, electronic_c2)
            .shift(wave_0_shift)
            .shift(UP * A_0 * np.sin(phi_0.get_value()))
        )

        base_line_1 = DashedLine(UP, DOWN).shift(wave_0_shift).set_color(GRAY)
        self.play(Create(electron), Create(base_line_1))

        def update_electronic(mob: Mobject):
            return mob.move_to(wave_0_shift + UP * A_0 * np.sin(phi_0.get_value()))

        electron.add_updater(update_electronic)
        self.play(
            phi_0.animate.set_value(-PI * 8), run_time=8, rate_func=linear
        )  # 符号是为了保证向右传播

        self.play(
            FadeOut(wave_0, base_line_1, electron, maxwell),
            year.animate.to_corner(DL),
        )

        electron.clear_updaters(True)
        wave_0.clear_updaters(True)

        num = 7
        A = 0.2
        t_range = (0, 10)
        electron.move_to(ORIGIN)
        electronics = [electron.copy() for _ in range(num)]
        elec_y = [(1.5 - 4 / (num - 1) * j) * UP for j in range(num)]
        wave_lenghts = [(PI / 5 + 9 * PI / 5 * j / (num - 1)) for j in range(num)]
        waves = []
        phi = ValueTracker(0)
        base_line_2 = (
            DashedLine(UP * 2, DOWN * 3).to_edge(LEFT, buff=LARGE_BUFF).set_color(GRAY)
        )

        for y, elec, wl in zip(elec_y, electronics, wave_lenghts):
            elec.shift(y).to_edge(LEFT, LARGE_BUFF - 0.1)

            def get_update_elec(y: Vector3D):
                def update_elec(mob: Mobject):
                    return mob.move_to(y + A * np.sin(phi.get_value()) * UP).to_edge(
                        LEFT, LARGE_BUFF - 0.1
                    )

                return update_elec

            elec.add_updater(get_update_elec(y))
            wave = (
                ParametricFunction(
                    lambda t: (t, np.sin(2 * PI / wl * t + phi.get_value()) * A, 0),
                    t_range=t_range,
                    color=sin_wl2color(wl),
                )
                .shift(y)
                .to_edge(LEFT, LARGE_BUFF)
            )

            def get_update_wave(y: Vector3D, wl: float):

                def update_wave(mob: Mobject):
                    return mob.become(
                        ParametricFunction(
                            lambda t: (
                                t,
                                np.sin(2 * PI / wl * t + phi.get_value()) * A,
                                0,
                            ),
                            t_range=t_range,
                            color=sin_wl2color(wl),
                        )
                        .shift(y)
                        .to_edge(LEFT, LARGE_BUFF)
                    )

                return update_wave

            wave.add_updater(get_update_wave(y, wl))
            waves.append(wave)

        self.play(
            Create(base_line_2),
            *[Create(elec) for elec in electronics],
            *[Create(wave) for wave in waves],
            run_time=2,
        )
        self.wait()

        self.play(phi.animate.set_value(-8 * PI), run_time=4, rate_func=linear)

        full_spectrum = get_full_spectrum()

        full_spectrum.scale_to_fit_height(5).shift(DOWN * 0.5).to_edge(
            RIGHT, LARGE_BUFF
        )
        full_sectrum_rect = SurroundingRectangle(full_spectrum).set_color(GRAY)

        self.play(
            FadeIn(full_spectrum, full_sectrum_rect),
            phi.animate.set_value(-12 * PI),
            run_time=2,
            rate_func=linear,
        )
        self.wait()
        self.play(Indicate(full_sectrum_rect))
        self.wait()
        self.play(
            FadeOut(
                *[elec for elec in electronics],
                *[wave for wave in waves],
                base_line_2,
                full_spectrum,
                full_sectrum_rect,
            )
        )

        rutherford = get_image("rutherford").to_edge(RIGHT)

        self.play(year.animate.set_value(1911).to_corner(DR), FadeIn(rutherford))
        nucleus_c1 = Circle(radius=0.15, color=RED)
        nucleus_c2 = Text("+", color=RED).scale(0.5)
        nucleus = VGroup(nucleus_c1, nucleus_c2)

        R_0 = 2
        radius_tracker = ValueTracker(R_0)
        angle_tracker = ValueTracker(0)

        # 轨道圆（半径随 radius_tracker 变化）
        orbit = Circle(radius=R_0, color=GRAY, stroke_width=1.5)
        orbit.add_updater(
            lambda c: c.become(
                Circle(radius=radius_tracker.get_value(), color=GRAY, stroke_width=1.5)
            )
        )
        electron.clear_updaters(True)
        electron.add_updater(
            lambda d: d.move_to(
                radius_tracker.get_value()
                * np.array(
                    [
                        np.cos(angle_tracker.get_value()),
                        np.sin(angle_tracker.get_value()),
                        0,
                    ]
                )
            )
        )
        self.play(FadeIn(nucleus, electron), Create(orbit))

        self.play(
            angle_tracker.animate.set_value(TAU * 2),
            run_time=6,
            rate_func=linear,
        )
        for _ in range(6):
            emit_pos = electron.get_center().copy()

            rings = VGroup()
            for init_r in [0.008, 0.02, 0.035]:
                ring = Circle(radius=init_r, stroke_color=BLUE_D, stroke_width=2)
                ring.move_to(emit_pos)
                rings.add(ring)

            self.play(
                Succession(
                    FadeIn(rings),
                    rings.animate.scale(40),  # pyright: ignore[reportArgumentType]
                    FadeOut(rings),
                ),
                angle_tracker.animate.set_value(angle_tracker.get_value() + TAU / 3),
                lag_ratio=0,
                run_time=1,
                rate_func=linear,
            )

        self.play(
            angle_tracker.animate.set_value(angle_tracker.get_value() + TAU * 4),
            radius_tracker.animate.set_value(0.3),
            run_time=5,
            rate_func=rate_functions.ease_in_sine,
        )
        # 撞击闪光
        flash = Circle(radius=0.5, color=WHITE, fill_opacity=0.6, fill_color=WHITE)
        flash.move_to(nucleus.get_center())
        self.play(FadeIn(flash, scale=3), run_time=0.2)
        self.play(FadeOut(flash), run_time=0.3)
        self.wait(0.5)

        self.wait()

        self.play(FadeOut(nucleus, electron, orbit, rutherford))

        self.next_section(skip_animations=_P["current"])

        hertz = get_image("hertz").to_edge(RIGHT)
        self.play(year.animate.set_value(1887), FadeIn(hertz))

        zinc_plate = Rectangle(
            width=2.5,
            height=4,
            fill_color="#C0C0C0",
            fill_opacity=0.6,
            stroke_color=GRAY,
        ).shift(RIGHT * 3.5)

        plate_label = Text("锌板", font_size=24, color=GRAY).next_to(
            zinc_plate, UP, buff=0.15
        )

        self.play(FadeIn(zinc_plate, plate_label))

        phi_1 = ValueTracker(0)
        A_1 = 0.2
        t_range_1 = (0, 6)
        uv_wl = 1
        ori_uv = ParametricFunction(
            lambda t: (t, A_1 * np.sin(2 * PI / uv_wl * t + phi_1.get_value()), 0),
            t_range=t_range_1,
            color=sin_wl2color(uv_wl),
        )
        uvs = [ori_uv.copy() for _ in range(3)]

        for i, uv in zip(range(3), uvs):
            uv.shift(UP * (1 - i) + LEFT * 3)

            def get_update_uv(cnt: int):
                def update_uv(mob: Mobject):
                    return mob.become(
                        ParametricFunction(
                            lambda t: (
                                t,
                                A_1 * np.sin(2 * PI / uv_wl * t + phi_1.get_value()),
                                0,
                            ),
                            t_range=t_range_1,
                            color=sin_wl2color(uv_wl),
                        )
                    ).shift(UP * (1 - cnt) + LEFT * 3)

                return update_uv

            uv.add_updater(get_update_uv(i))

        self.play(
            FadeIn(*uvs),
        )

        self.play(phi_1.animate.set_value(-PI * 4), run_time=4, rate_func=linear)

        self.wait()  # SchrodingerEquation
