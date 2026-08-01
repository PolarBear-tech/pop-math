from typing import override

from manim import *
import numpy as np


class RutherfordProblem(Scene):
    @override
    def construct(self):
        Text.set_default(font="LXGW WenKai")

        # ================================================================
        # Act 1: 标题
        # ================================================================
        title = Text("卢瑟福原子模型", font_size=48)
        year = Text("1911年  —  太阳系模型", font_size=36, color=YELLOW)
        subtitle = Text("原子核带正电，电子绕核运动", font_size=28, color=GRAY)
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
        # Act 2: 展示原子模型
        # ================================================================
        # 原子核
        nucleus = Circle(radius=0.25, color=YELLOW, fill_opacity=1, fill_color=YELLOW)
        nucleus_label = Text("原子核", font_size=24, color=YELLOW).next_to(nucleus, UP, buff=0.15)
        nucleus_group = VGroup(nucleus, nucleus_label)

        R0 = 3.0
        angle_tracker = ValueTracker(0)
        radius_tracker = ValueTracker(R0)

        # 轨道圆（半径随 radius_tracker 变化）
        orbit = Circle(radius=R0, color=GRAY, stroke_width=1.5)
        orbit.add_updater(
            lambda c: c.become(
                Circle(radius=radius_tracker.get_value(), color=GRAY, stroke_width=1.5)
            )
        )

        # 电子（位置随 angle 和 radius 变化）
        electron = Dot(radius=0.1, color=BLUE)
        electron.add_updater(
            lambda d: d.move_to(
                radius_tracker.get_value()
                * np.array([np.cos(angle_tracker.get_value()), np.sin(angle_tracker.get_value()), 0])
            )
        )
        electron_label = Text("电子", font_size=22, color=BLUE)
        electron_label.add_updater(lambda d: d.next_to(electron, UR, buff=0.08))

        self.play(FadeIn(nucleus_group, scale=0.5))
        self.wait(0.3)
        self.play(Create(orbit))
        self.wait(0.3)
        self.play(FadeIn(electron, scale=0.5), FadeIn(electron_label))
        self.wait(0.5)

        # 模型文字说明
        model_text = Text(
            "卢瑟福认为：原子结构与太阳系类似\n"
            "电子在库仑力作用下绕核做圆周运动",
            font_size=26,
            line_spacing=1.5,
        )
        model_text.to_edge(UP, buff=0.5)
        self.play(Write(model_text))

        # 电子绕核旋转若干圈
        self.play(
            angle_tracker.animate.set_value(TAU * 4),
            run_time=6,
            rate_func=linear,
        )

        # ================================================================
        # Act 3: 经典电磁理论的矛盾
        # ================================================================
        problem_text = Text(
            "经典电磁理论：加速电荷会辐射电磁波\n"
            "→ 电子能量不断损失，轨道持续缩小",
            font_size=26,
            color=RED,
            line_spacing=1.5,
        )
        problem_text.next_to(model_text, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play(FadeOut(model_text))
        self.play(Write(problem_text))

        # 电子继续旋转，同时从电子位置发出辐射波纹
        for _ in range(6):
            target_angle = angle_tracker.get_value() + TAU / 3
            emit_pos = electron.get_center().copy()

            rings = VGroup()
            for init_r in [0.08, 0.2, 0.35]:
                ring = Circle(radius=init_r, stroke_color=BLUE_D, stroke_width=2)
                ring.move_to(emit_pos)
                rings.add(ring)

            self.add(rings)
            self.play(
                angle_tracker.animate.set_value(target_angle),
                *[ring.animate.scale(4).set_stroke_opacity(0) for ring in rings],
                run_time=1.2,
                rate_func=smooth,
            )
            self.remove(rings)

        # ================================================================
        # Act 4: 螺旋坠落
        # ================================================================
        collapse_text = Text("最终：电子坠入原子核！", font_size=30, color=RED)
        collapse_text.next_to(problem_text, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(collapse_text))

        # 半径逐渐缩小 → 螺旋效果
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

        # 淡出除原子核外的所有元素
        self.play(
            FadeOut(problem_text),
            FadeOut(collapse_text),
            FadeOut(electron),
            FadeOut(electron_label),
            FadeOut(orbit),
        )

        # ================================================================
        # Act 5: 提出问题
        # ================================================================
        bg = FullScreenRectangle(color=BLACK, fill_opacity=0.8)
        self.add(bg)

        question = Text(
            "那么…… 为什么原子是稳定的？",
            font_size=48,
            color=RED,
            line_spacing=1.5,
        )
        self.play(Write(question))
        self.wait(4)
        self.play(FadeOut(VGroup(bg, question)))
        self.wait(1)
