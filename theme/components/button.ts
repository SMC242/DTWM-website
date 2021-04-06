import { ComponentStyleConfig } from "@chakra-ui/react";
import { mode } from "@chakra-ui/theme-tools";

const Button: ComponentStyleConfig = {
  baseStyle: {
    background: "initial", // <---- this resets the background to whatever normal value it has
    bgGradient: "linear(to-b, pink.500, purple.500)",
  },
};
export default Button;
