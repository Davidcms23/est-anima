from manim import *

VALORES_INICIAIS = [2, 5, 3, 7, 4, 3]
CORES = [BLUE_D, TEAL_D, GREEN_D, YELLOW_D, ORANGE, RED_D, PURPLE_D, PINK]


class MediaDinamica(Scene):
    def construct(self):
        n = len(VALORES_INICIAIS)

        reta = NumberLine(
            x_range=[0, 10, 1],
            length=10.5,
            include_numbers=False,
        )
        reta.move_to(DOWN * 1.2)
        numeros = VGroup(
            *[Text(str(i), font_size=20).next_to(reta.n2p(i), DOWN, buff=0.2) for i in range(0, 11)]
        )
        self.play(Create(reta), FadeIn(numeros), run_time=1.0)

        # um ValueTracker por ponto: a "fonte da verdade" de cada valor
        trackers = [ValueTracker(v) for v in VALORES_INICIAIS]

        def media_atual():
            return sum(t.get_value() for t in trackers) / n

        # bolinhas que seguem seus trackers
        pontos = VGroup()
        for i, t in enumerate(trackers):
            dot = Dot(radius=0.16, color=CORES[i % len(CORES)])
            dot.move_to(reta.n2p(t.get_value()))
            dot.add_updater(lambda d, t=t: d.move_to(reta.n2p(t.get_value())))
            pontos.add(dot)

        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in pontos], lag_ratio=0.15), run_time=1.2)
        self.wait(0.3)

        # ponto invisível que sempre fica na posição da média
        marcador_media = Dot(radius=0, fill_opacity=0)
        marcador_media.move_to(reta.n2p(media_atual()))
        marcador_media.add_updater(lambda m: m.move_to(reta.n2p(media_atual())))
        self.add(marcador_media)

        rastro = TracedPath(
            marcador_media.get_center,
            stroke_color=RED,
            stroke_width=3,
            stroke_opacity=0.5,
        )
        self.add(rastro)

        fulcro = Triangle(fill_color=RED, fill_opacity=1, stroke_width=0)
        fulcro.set_height(0.35)
        fulcro.add_updater(lambda f: f.next_to(marcador_media, DOWN, buff=0.45))

        rotulo = always_redraw(
            lambda: Text(f"x̄ = {media_atual():.2f}", font_size=28, color=RED).next_to(
                marcador_media, UP, buff=0.35
            )
        )

        self.play(GrowFromCenter(fulcro), FadeIn(rotulo), run_time=0.8)
        self.wait(0.8)

        # --- Equação com traço de fração (\frac) em altura rebaixada ---
        FS = 26

        def criar_equacao_fracao():
            x_barra = Text("x̄ =", font_size=FS)

            # Numerador: termos dinâmicos com os sinais de +
            num_group = VGroup()
            for i in range(n):
                val_txt = Text(f"{trackers[i].get_value():.1f}", font_size=FS, color=CORES[i])
                num_group.add(val_txt)
                if i < n - 1:
                    plus_txt = Text("+", font_size=FS)
                    num_group.add(plus_txt)
            num_group.arrange(RIGHT, buff=0.14)

            # Denominador
            den_txt = Text(str(n), font_size=FS)

            # Linha de fração
            largura_frac = num_group.width + 0.3
            barra_fracao = Line(LEFT * (largura_frac / 2), RIGHT * (largura_frac / 2), stroke_width=2.5)

            # Empilha numerador, linha e denominador
            bloco_fracao = VGroup(num_group, barra_fracao, den_txt)
            num_group.next_to(barra_fracao, UP, buff=0.12)
            den_txt.next_to(barra_fracao, DOWN, buff=0.12)

            igual = Text("=", font_size=FS)
            media_txt = Text(f"{media_atual():.2f}", font_size=FS, color=RED)

            eq = VGroup(x_barra, bloco_fracao, igual, media_txt).arrange(RIGHT, buff=0.22)
            # Altura rebaixada (ao invés de ficar colada no topo via to_edge)
            eq.move_to(UP * 1.5)
            return eq

        equacao = always_redraw(criar_equacao_fracao)

        self.play(FadeIn(equacao, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.8)

        # --- Rodada 1: um ponto se afasta bastante (efeito moderado) ---
        self.play(trackers[3].animate.set_value(9.5), run_time=2.2, rate_func=smooth)
        self.wait(0.8)

        # --- Rodada 2: vários pontos mudam ao mesmo tempo, convergindo ---
        alvos_2 = [4, 4.5, 5, 6, 5.5, 4]
        self.play(
            *[trackers[i].animate.set_value(alvos_2[i]) for i in range(n)],
            run_time=2.2,
            rate_func=smooth,
        )
        self.wait(0.8)

        # --- Rodada 3: os pontos se espalham de forma assimétrica ---
        alvos_3 = [1, 2, 3, 8, 8.5, 1.5]
        self.play(
            *[trackers[i].animate.set_value(alvos_3[i]) for i in range(n)],
            run_time=2.5,
            rate_func=smooth,
        )
        self.wait(1.0)

        # --- Rodada 4: Outlier Extremo (valor 100) ---
        # Um dos pontos dispara para 100, puxando a média visivelmente para fora do visor da reta
        self.play(
            trackers[3].animate.set_value(100.0),
            run_time=3.5,
            rate_func=smooth,
        )
        self.wait(2.0)

        for m in [*pontos, marcador_media, fulcro]:
            m.clear_updaters()

        self.play(
            FadeOut(pontos),
            FadeOut(fulcro),
            FadeOut(rotulo),
            FadeOut(rastro),
            FadeOut(reta),
            FadeOut(numeros),
            FadeOut(equacao),
            run_time=0.8,
        )
