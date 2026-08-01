from typing import override

from manim import *
import numpy as np


class PhotoelectricEffect(Scene):
    @override
    def construct(self) -> None:
        Text.set_default(font="LXGW WenKai")

        # ================================================================
        # Act 1: 标题
        # ================================================================
        title = Text("光电效应", font_size=48)
        year = Text("1887年  —  赫兹的发现", font_size=36, color=YELLOW)
        subtitle = Text(
            "当光照射到金属表面时，电子会从表面逸出", font_size=28, color=GRAY
        )
        title.to_edge(UP, buff=1.5)
        year.next_to(title, DOWN, buff=0.4)
        subtitle.next_to(year, DOWN, buff=0.2)

        self.play(Write(title))
        self.wait(0.3)
        self.play(Write(year))
        self.wait(0.3)
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(VGroup(title, year, subtitle)))
        self.wait(0.5)

        # ================================================================
        # Act 2: 实验装置 — 锌板
        # ================================================================
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

        base = Rectangle(
            width=4, height=0.25, fill_color=GRAY, fill_opacity=0.8, stroke_color=GRAY
        ).next_to(zinc_plate, DOWN, buff=0)

        self.play(
            FadeIn(zinc_plate, scale=0.5),
            FadeIn(plate_label),
            Create(base),
        )
        self.wait(0.5)

        annotation = Text(
            "* 本演示为概念示意，非真实实验装置", font_size=16, color=GRAY
        ).to_edge(DOWN, buff=SMALL_BUFF)
        self.play(FadeIn(annotation))

        # ================================================================
        # Act 3: 紫外线实验
        # ================================================================
        uv_label = Text("紫外线", font_size=24, color=PURPLE).to_corner(UL, buff=1)

        uv_arrows = VGroup()
        for y in np.linspace(-1.5, 1.5, 5):
            start = LEFT * 2.5 + UP * y
            end = zinc_plate.get_left() + UP * y * 0.25
            arrow = Arrow(start, end, color=PURPLE, stroke_width=3, buff=0)
            uv_arrows.add(arrow)

        self.play(Write(uv_label))
        self.play(Create(uv_arrows), run_time=1)
        self.wait(0.5)

        electron_template = VGroup(
            Circle(0.1, color=BLUE),
            Text("-", color=BLUE).scale(0.5),
        )

        electrons = VGroup()
        for dy in [-1.2, -0.4, 0.4, 1.2]:
            pos = zinc_plate.get_right() + RIGHT * 0.3 + UP * dy
            e = electron_template.copy().move_to(pos)
            electrons.add(e)

        uv_result = Text("✓ 电子溢出！", font_size=28, color=GREEN).next_to(
            zinc_plate, RIGHT, buff=0.5
        )

        self.play(
            LaggedStart(
                *[FadeIn(e, shift=RIGHT * 0.3) for e in electrons],
                lag_ratio=0.15,
            ),
            FadeIn(uv_result, shift=UP),
        )
        self.wait(1)

        self.play(
            *[e.animate.shift(RIGHT * 0.8).set_opacity(0) for e in electrons],
        )
        self.wait(0.5)
        self.play(FadeOut(uv_arrows, uv_label, uv_result))

        # ================================================================
        # Act 4: 红光实验（亮度相同甚至更高）
        # ================================================================
        red_label = Text("红光（亮度更高）", font_size=24, color=RED).to_corner(
            UL, buff=1
        )

        red_arrows = VGroup()
        for y in np.linspace(-1.8, 1.8, 7):
            start = LEFT * 2.5 + UP * y
            end = zinc_plate.get_left() + UP * y * 0.25
            arrow = Arrow(start, end, color=RED, stroke_width=5, buff=0)
            red_arrows.add(arrow)

        energy_note = Text("* 能量更多 → 亮度更高", font_size=16, color=RED).next_to(
            annotation, UP, buff=0.1
        )
        self.play(FadeIn(energy_note))

        self.play(Write(red_label))
        self.play(Create(red_arrows), run_time=1)
        self.wait(2)

        no_result = Text("✗ 无电子溢出……", font_size=28, color=RED).next_to(
            zinc_plate, RIGHT, buff=0.5
        )
        self.play(FadeIn(no_result, shift=UP))
        self.wait(1.5)

        question = Text(
            "明明能量更多了，电子哪儿去了？", font_size=36, color=YELLOW
        ).to_edge(DOWN, buff=1)
        self.play(Write(question))
        self.wait(3)

        # ================================================================
        # Act 5: 谜团
        # ================================================================
        self.play(
            FadeOut(
                VGroup(
                    red_arrows,
                    red_label,
                    no_result,
                    question,
                    energy_note,
                    annotation,
                    zinc_plate,
                    plate_label,
                    base,
                )
            )
        )

        mystery = Text(
            "这个谜团困扰了物理学家们几十年……",
            font_size=40,
            color=RED,
        )
        self.play(Write(mystery))
        self.wait(4)
        self.play(FadeOut(mystery))
        self.wait(1)
