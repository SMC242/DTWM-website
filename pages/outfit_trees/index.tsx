import Head from "next/head";
import Link from "next/link";
import React from "react";
import { UnorderedList, ListItem, Heading } from "@chakra-ui/react";

import Article from "../../components/templates/article";
import Header from "../../components/templates/header";

const OutfitTreesHomePage = () => {
  const trees = [{ name: "MB1", route: "/outfit_trees/MB1" }];
  return (
    <>
      <Header
        site_name="DTWM - Outfit Trees"
        description="List of the compiled outfit trees."
        title="Outfit Tree Home Page"
      />
      <Article>
        <Heading>Available outfit family trees</Heading>
        <UnorderedList>
          {trees.map((t) => (
            <ListItem textDecoration="underline">
              <Link key={t.name} href={t.route}>
                <a key={t.name}>{t.name}</a>
              </Link>
            </ListItem>
          ))}
        </UnorderedList>
      </Article>
    </>
  );
};

export default OutfitTreesHomePage;
