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
  NavbarStack: {
    baseStyle: {
      // color: mode("blackAlpha-900", "pink.400"), // for the upcoming dark theme changes
    },
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
