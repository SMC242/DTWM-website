import { mode } from "@chakra-ui/theme-tools";

const styles = {
  global: (props: object) => ({
    body: {
      bg: mode("gray.50", "blue.800")(props),
    },
  }),
};

export default styles;
