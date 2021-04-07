import { mode } from "@chakra-ui/theme-tools";
import { ComponentStyleConfig } from "@chakra-ui/react";

export const QuoteBlock: ComponentStyleConfig = {
  baseStyle: {
    _before: {
      color: "#ccc",
      content: "open-quote",
      marginRight: "0.25em",
      fontSize: "4em",
      lineHeight: "0.1em",
    },
  },
};
