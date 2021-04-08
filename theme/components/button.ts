import { ComponentStyleConfig } from "@chakra-ui/react";
import { mode } from "@chakra-ui/theme-tools";

export const Button: ComponentStyleConfig = {
  baseStyle: {
    margin: "0.5",
  },
};

export const MainButton: ComponentStyleConfig = {
  baseStyle: (props) => ({
    bgGradient: mode(
      "linear(to-t, yellow.500, orange.300)",
      "linear(to-b, pink.500, purple.500)"
    )(props),
    bg: mode(undefined, "unset")(props),
    _hover: { filter: "invert(100%" },
  }),
};
