import React from "react";
import { Text, Heading } from "@chakra-ui/react";

import Article from "../../components/templates/article";
import Tree from "../../components/outfit_tree/tree";
import MB1 from "../../components/outfit_tree/outfits/MB1";
import Header from "../../components/templates/header";

const MB1FamilyTree = () => {
  return (
    <>
      <Header
        title="MB1 Family Tree"
        description="The outfit split history of MB1"
      />
      <Article>
        <Heading>Info</Heading>
        <Text>
          This is the history of MB1 and its children as I understand it
        </Text>
        <Text>Last update: 2021-05-27 11:21</Text>
        <Tree nodes={MB1} />
      </Article>
    </>
  );
};

export default MB1FamilyTree;
