import React, { FC, PropsWithChildren } from "react";
import {
  Text,
  useStyleConfig,
  TextProps,
  HStack,
  chakra,
} from "@chakra-ui/react";

export interface QuoteProps extends TextProps {}

const BlockQuote = chakra("blockquote");

const Quote: FC<PropsWithChildren<QuoteProps>> = ({
  size,
  variant,
  children,
  ...props
}) => {
  const block_styles = useStyleConfig("QuoteBlock", { size, variant });

  return (
    <HStack>
      <BlockQuote sx={block_styles}>
        <Text {...props}>{children}</Text>
      </BlockQuote>
    </HStack>
  );
};

export default Quote;
