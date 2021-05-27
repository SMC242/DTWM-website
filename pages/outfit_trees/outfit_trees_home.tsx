import Head from "next/head";
import Link from "next/link";
import React from "react";
import { UnorderedList, ListItem, Heading } from "@chakra-ui/react";

import Article from "../../components/templates/article";
import OG from "../../components/templates/open_graph";

const OutfitTreesHomePage = () => {
  const trees = [{ name: "MB1", route: "/outfit_trees/MB1" }];
  return (
    <>
      <Head>
        <title>Outfit Tree Home Page</title>
        <OG
          site_name="DTWM - Outfit Trees"
          description="List of the compiled outfit trees."
        />
      </Head>
      <Article>
        <Heading>Available outfit family trees</Heading>
        <UnorderedList>
          {trees.map((t) => (
            <ListItem textDecoration="underline">
              <Link key={t.name} href={t.route}>
                <a>{t.name}</a>
              </Link>
            </ListItem>
          ))}
        </UnorderedList>
      </Article>
    </>
  );
};

export default OutfitTreesHomePage;
