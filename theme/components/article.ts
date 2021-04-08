import { mode } from "@chakra-ui/theme-tools";
import { ComponentStyleConfig } from "@chakra-ui/react";

const Article: ComponentStyleConfig = {
  baseStyle: (props) => ({
    bg: mode("gray.100", "blackAlpha.300")(props),
    minWidth: "66%",
    padding: "1em",
  }),
};

export default Article;
