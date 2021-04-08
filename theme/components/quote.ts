import { mode } from "@chakra-ui/theme-tools";
import { ComponentStyleConfig } from "@chakra-ui/react";

export const QuoteBlock: ComponentStyleConfig = {
  baseStyle: (props) => ({
    borderColor: mode("yellow.400", "gray.50")(props),
    borderLeftWidth: "0.2em",
    paddingLeft: "0.8em",
  }),
};
