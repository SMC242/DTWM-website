import { mode } from "@chakra-ui/theme-tools";

type LayerStyle = (props: Record<string, any>) => any;

const layerStyles: Record<string, LayerStyle> = {
  base: (props) => ({
    bg: mode("gray.100", "blackAlpha.300")(props),
  }),
  top: (props) => ({
    bg: mode("yellow.500", "blue.900")(props),
  }),
};

export default layerStyles;
