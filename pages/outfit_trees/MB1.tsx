import React from "react";
import Head from "next/head";
import { Text, Heading } from "@chakra-ui/react";

import Article from "../../components/templates/article";
import Tree from "../../components/outfit_tree/tree";
import MB1 from "../../components/outfit_tree/outfits/MB1";

const MB1FamilyTree = () => {
  return (
    <>
      <Head>
        <title>MB1 Family Tree</title>
      </Head>
      <Article>
        <Heading>Info</Heading>
        <Text>
          This is the history of MB1 and its children as I understand it
        </Text>
        <Text>Last update: 2021-05-23 03:22</Text>
        <Tree nodes={MB1} />
      </Article>
    </>
  );
};

export default MB1FamilyTree;
