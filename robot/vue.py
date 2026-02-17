class VueTerminal:

    def dessiner_robot(self, robot):
        print(
            f"Robot -> x={robot.x:.2f}, "
            f"y={robot.y:.2f}, "
            f"orientation={robot.orientation:.2f}"
        )        