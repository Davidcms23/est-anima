from manim import *

VALORES_INICIAIS = [2, 5, 3, 7, 4, 3]
CORES = [BLUE_D, TEAL_D, GREEN_D, YELLOW_D, ORANGE, RED_D, PURPLE_D, PINK]


class MediaDinamica(Scene):
    def construct(self):
        n = len(VALORES_INICIAIS)

        trackers = [ValueTracker(v) for v in VALORES_INICIAIS]

        x_max_tracker = ValueTracker(10.0)

        def media_atual():
            return sum(t.get_value() for t in trackers) / n

        LARGURA_RETA = 10.5
        Y_RETA = -1.3
        ORIGEM_X = -5.25

        def valor_para_ponto(v):
            x_max = x_max_tracker.get_value()
            prop = v / x_max
            return np.array([ORIGEM_X + prop * LARGURA_RETA, Y_RETA, 0])

        def criar_sistema_reta():
            x_max = x_max_tracker.get_value()
            p_origem = np.array([ORIGEM_X, Y_RETA, 0])
            p_fim = np.array([ORIGEM_X + LARGURA_RETA, Y_RETA, 0])

            linha = Line(p_origem, p_fim, stroke_width=3, color=WHITE).set_z_index(0)

            ticks_e_rotulos = VGroup()
            passo = 1 if x_max <= 12 else (5 if x_max <= 30 else 10)

            for val in range(0, int(x_max) + 1, passo):
                pos = valor_para_ponto(val)
                tick = Line(pos + UP * 0.08, pos + DOWN * 0.08, stroke_width=2, color=WHITE)
                txt = Text(str(val), font_size=16 if passo == 1 else 13)
                txt.next_to(tick, DOWN, buff=0.18)
                ticks_e_rotulos.add(tick, txt)

            return VGroup(linha, ticks_e_rotulos)

        sistema_reta = always_redraw(criar_sistema_reta)
        self.add(sistema_reta)

        def raio_dinamico():
            fator = 10.0 / x_max_tracker.get_value()
            return max(0.08, 0.16 * (fator ** 0.45))

        pontos = VGroup()
        for i, t in enumerate(trackers):
            ponto = always_redraw(
                lambda i=i, t=t: Dot(
                    point=valor_para_ponto(t.get_value()),
                    radius=raio_dinamico(),
                    color=CORES[i % len(CORES)],
                ).set_z_index(3)
            )
            pontos.add(ponto)

        self.play(FadeIn(pontos), run_time=1.0)
        self.wait(0.3)

        linha_media = always_redraw(
            lambda: DashedLine(
                start=valor_para_ponto(media_atual()) + DOWN * 0.16,
                end=valor_para_ponto(media_atual()) + UP * 1.0,
                color=RED,
                stroke_width=3,
                dash_length=0.08,
            ).set_z_index(2)
        )

        self.play(Create(linha_media), run_time=0.8)
        self.wait(0.5)

        FS = 24

        def criar_equacao():
            x_barra = Text("x̄ =", font_size=FS)

            num_group = VGroup()
            for i in range(n):
                val_txt = Text(f"{trackers[i].get_value():.1f}", font_size=FS, color=CORES[i])
                num_group.add(val_txt)
                if i < n - 1:
                    plus_txt = Text("+", font_size=FS)
                    num_group.add(plus_txt)
            num_group.arrange(RIGHT, buff=0.12)

            den_txt = Text(str(n), font_size=FS)
            largura_barra = num_group.width + 0.25
            barra = Line(LEFT * (largura_barra / 2), RIGHT * (largura_barra / 2), stroke_width=2)

            bloco_frac = VGroup(num_group, barra, den_txt)
            num_group.next_to(barra, UP, buff=0.1)
            den_txt.next_to(barra, DOWN, buff=0.1)

            igual = Text("=", font_size=FS)
            media_txt = Text(f"{media_atual():.2f}", font_size=FS, color=RED)

            eq = VGroup(x_barra, bloco_frac, igual, media_txt).arrange(RIGHT, buff=0.2)
            eq.move_to(UP * 1.5)
            return eq

        equacao = always_redraw(criar_equacao)
        self.play(FadeIn(equacao, shift=DOWN * 0.2), run_time=0.8)
        self.wait(0.8)

        self.play(trackers[3].animate.set_value(9.5), run_time=2.0, rate_func=smooth)
        self.wait(0.8)

        alvos_2 = [4, 4.5, 5, 6, 5.5, 4]
        self.play(
            *[trackers[i].animate.set_value(alvos_2[i]) for i in range(n)],
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(0.8)

        alvos_3 = [1, 2, 3, 8, 8.5, 1.5]
        self.play(
            *[trackers[i].animate.set_value(alvos_3[i]) for i in range(n)],
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(1.0)

        trackers[3].add_updater(lambda t: t.set_value(x_max_tracker.get_value()))

        self.play(
            x_max_tracker.animate.set_value(100.0),
            run_time=5.0,
            rate_func=smooth,
        )
        trackers[3].clear_updaters()
        self.wait(2.5)

        for obj in self.mobjects:
            obj.clear_updaters()

        self.play(FadeOut(*self.mobjects), run_time=0.8)
