import { extendTheme, ChakraProvider, ThemeOverride } from "@chakra-ui/react";
import React, { FC, PropsWithChildren } from "react";
import colours from "./colours";
import theme_config from "./config";
import styles from "./styles";

const overrides: ThemeOverride = {
  styles,
  components: {},
};

export const Theme = extendTheme({
  colors: colours,
  config: theme_config,
  overrides,
});

export const CustomChakraProvider: FC<PropsWithChildren<{}>> = ({
  children,
}) => <ChakraProvider theme={Theme}>{children}</ChakraProvider>;
