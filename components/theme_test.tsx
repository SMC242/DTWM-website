import React from "react";
import { Box, Divider, Text } from "@chakra-ui/react";
import { MainButton } from "./inputs/btn";

const template = (
  first: number,
  second: number,
  third: number,
  fourth: number
): string => `${first}.${second}.${third}.${fourth}`;
const random = (column: number) => Math.floor(Math.random() * column);
const ip_address = template(random(100), random(100), random(10), random(10));

const ThemeTest = () => {
  return (
    <Box mx="5">
      <MainButton colorScheme="yellow">UmU</MainButton>
      <MainButton>AwA</MainButton>
      <Divider my="5" />
      <Text>Now I have your IP address mwahahahahahahahahahaha!</Text>
      <Text>It is: {ip_address}</Text>
      <Divider my="5" />
      <Text>
        <small>I haven't actually grabbed your IP :)</small>
      </Text>
      <Text>
        <small>Refresh the page.</small>
      </Text>
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
      <br />
    </Box>
  );
};

export default ThemeTest;
