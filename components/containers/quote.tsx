import React, { FC, PropsWithChildren, CSSProperties } from "react";
import {
  Text,
  useStyleConfig,
  TextProps,
  HStack,
  chakra,
} from "@chakra-ui/react";

export interface QuoteProps extends TextProps {}

const BlockQuote = chakra("blockquote", {
  baseStyle: {
    borderLeft: "10px solid #ccc",
  },
});

const Quote: FC<PropsWithChildren<QuoteProps>> = ({
  size,
  variant,
  children,
  ...props
}) => {
  const text_styles = useStyleConfig("QuoteText", { size, variant });
  const block_styles = useStyleConfig("QuoteBlock", { size, variant });
  return (
    <HStack>
      <BlockQuote sx={block_styles}>
        <Text sx={text_styles} {...props}>
          {children}
        </Text>
      </BlockQuote>
    </HStack>
  );
};

export default Quote;
