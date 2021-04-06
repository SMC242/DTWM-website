import React from "react";
import { Box, Button, useColorMode } from "@chakra-ui/react";

const ThemeTest = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <Box>
      <Button colorScheme="yellow">UmU</Button>
      <Button colorScheme="blue">AwA</Button>
      <Button colorScheme="pink" onClick={toggleColorMode}>
        Switch theme. Current mode: {colorMode}
      </Button>
    </Box>
  );
};

export default ThemeTest;
