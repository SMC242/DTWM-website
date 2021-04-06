import { extendTheme, ChakraProvider, ThemeConfig } from "@chakra-ui/react";
import React, { FC, PropsWithChildren } from "react";

const colours = {
  blue: {
    "50": "#E5E5FF",
    "100": "#B8B8FF",
    "200": "#8A8AFF",
    "300": "#5C5CFF",
    "400": "#2E2EFF",
    "500": "#0000FF",
    "600": "#0000CC",
    "700": "#000099",
    "800": "#000066",
    "900": "#000033",
  },
  yellow: {
    "50": "#FFFCE5",
    "100": "#FFF8B8",
    "200": "#FFF38A",
    "300": "#FFEF5C",
    "400": "#FFEA2E",
    "500": "#FFE600",
    "600": "#CCB800",
    "700": "#998A00",
    "800": "#665C00",
    "900": "#332E00",
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
