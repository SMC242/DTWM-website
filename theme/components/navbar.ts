import { ComponentStyleConfig } from "@chakra-ui/react";
import { mode } from "@chakra-ui/theme-tools";

const NavbarStyles: Record<string, ComponentStyleConfig> = {
  NavbarContainer: {
    baseStyle: {
      marginBottom: "4rem",
    },
  },
  NavbarBG: {
    baseStyle: (props) => ({
      bg: mode("yellow.500", "blue.900")(props),
      w: "100%",
    }),
  },
  NavbarGrid: {
    baseStyle: {
      alignItems: "center",
    },
  },
  NavbarButton: {
    baseStyle: (props) => ({
      color: mode("blackAlpha-900", "pink.300")(props), // for the upcoming dark theme changes
    }),
  },
  NavItemBox: {
    baseStyle: {
      h: "100%",
      d: "inline",
      mx: "2",
    },
  },
};

export default NavbarStyles;
