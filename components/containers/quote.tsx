import React, { FC, PropsWithChildren } from "react";
import { Text, useStyleConfig, TextProps, HStack } from "@chakra-ui/react";

export interface QuoteProps extends TextProps {}

interface QuoteRectangleProps {
  height?: number | string;
  width: number | string;
}

const QuoteRectangle: FC<QuoteRectangleProps> = ({ height, width }) => (
  <svg viewBox="0 0 2 10" width={width} height={height}>
    <rect width="20%" height="100%" style={{ fill: "#FFFFFF" }}></rect>
  </svg>
);

const Quote: FC<PropsWithChildren<QuoteProps>> = ({
  size,
  variant,
  children,
  ...props
}) => {
  const styles = useStyleConfig("Quote", { size, variant });
  return (
    <HStack>
      <QuoteRectangle width="1em" height="100%" />
      <Text sx={styles} {...props}>
        {children}
      </Text>
    </HStack>
  );
};

export default Quote;
