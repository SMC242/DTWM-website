import { extendTheme, ChakraProvider, ThemeConfig } from "@chakra-ui/react";
import React, { FC, PropsWithChildren } from "react";

const colours = {
  main: {
    blue: "#012168",
    blue_dark: "#000042",
    highlight_yellow: "#fde40",
    highlight_yellow_dark: "#d47700",
  },
};

const theme_config: ThemeConfig = {
  initialColorMode: "dark",
  useSystemColorMode: true,
};

const portal_z_index = 20;

export const Theme = extendTheme({
  colors: colours,
  themeConfig: theme_config,
});

export const CustomChakraProvider: FC<PropsWithChildren<{}>> = ({
  children,
}) => (
  <ChakraProvider portalZIndex={portal_z_index} theme={Theme}>
    {children}
  </ChakraProvider>
);
