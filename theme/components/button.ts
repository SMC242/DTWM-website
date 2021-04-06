import { ComponentStyleConfig } from "@chakra-ui/react";
import { mode } from "@chakra-ui/theme-tools";

const Button: ComponentStyleConfig = {
  baseStyle: (props: object) => ({
    bgGradient: mode(
      "linear(to-b, pink.500, purple.500)",
      "linear(to-b, green.200, red.300)"
    )(props),
  }),
};
export default Button;
