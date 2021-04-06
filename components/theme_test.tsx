import React from "react";
import { Box, useColorMode, Divider, Text } from "@chakra-ui/react";
import { MainButton } from "./inputs/btn";

const template = (
  first: number,
  second: number,
  third: number,
  fourth: number
): string => `${first}.${second}.${third}.${fourth}`;
const random = (column: number) => Math.floor(Math.random() * column);
const get_ip_address = () =>
  template(random(100), random(100), random(10), random(10));

const ThemeTest = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <Box mx="5">
      <MainButton colorScheme="yellow">UmU</MainButton>
      <MainButton>AwA</MainButton>
      <Divider my="5" />
      <Text>Now I have your IP adress mwahahahahahahahahahaha!</Text>
      <Text>It is: {get_ip_address()}</Text>
      <Divider my="5" />
      <Text>
        <small>I haven't actually grabbed your IP :)</small>
      </Text>
      <Text>
        <small>Refresh the page.</small>
      </Text>
    </Box>
  );
};

export default ThemeTest;
