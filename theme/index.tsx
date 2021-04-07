import { extendTheme, ChakraProvider, ThemeOverride } from "@chakra-ui/react";
import React, { FC, PropsWithChildren } from "react";
import colours from "./colours";
import theme_config from "./config";
import styles from "./styles";
import { Button, MainButton } from "./components/button";
import font_theme from "./fonts";

const overrides: ThemeOverride = {
  colors: colours,
  config: theme_config,
  styles,
  ...font_theme,
  components: { Button, MainButton },
};

export const Theme = extendTheme(overrides);

export const CustomChakraProvider: FC<PropsWithChildren<{}>> = ({
  children,
}) => <ChakraProvider theme={Theme}>{children}</ChakraProvider>;
