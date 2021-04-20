import React from "react";
import { Text, Heading, UnorderedList, ListItem } from "@chakra-ui/react";
import Article from "../components/templates/article";
import Quote from "../components/containers/quote";
import Link from "next/link";

const Info = () => (
  <Article>
    <Heading>Who are DTWM?</Heading>
    <Quote>
      Some call us weebs. Others call us bronies. Many call us teamkillers.
      Ajfejkewgbjkewjkgewhghjggjeggejjgehejgswlgejlswkgjklsssssssssssssssss
      Please calklgjkejkfhee an ambuleance ben teamkilledgj me again
    </Quote>
    <Text>
      DTWM is a combined arms midfit founded in 2019. This means that we focus
      on using vehicles and infantry in tandem to capture bases. We also aim to
      be worth far more population than we have.
    </Text>
    <Heading>What is DTWM's playstyle?</Heading>
    <UnorderedList>
      <ListItem>
        We are serious when it counts during ops, but messing around is allowed
        when it doesn't matter
      </ListItem>
      <ListItem>
        We emphasise initiative and speed to outplay slower forces
      </ListItem>
      <ListItem>
        Those who want to learn to lead are encouraged and supported to do so
      </ListItem>
    </UnorderedList>
    <Heading>How is DTWM's community managed?</Heading>
    <Text>
      The hierarchy is kept fairly flat. Members get to vote on any important
      decisions and may repeal any decision made by leaders. The smaller
      decisions are handled by a council of leaders. All members are encouraged
      to drop into Council meetings and have an equal say with leaders. ANVILs
      and facility modules are available to long-standing members.
    </Text>
    <Heading>Schedule</Heading>
    <Text>
      We have 2 - 6 ops per week. The schedule is announced weekly on a Sunday
      or Monday.
    </Text>
    <Text>
      We also do trainings on Jaeger - a closed server - every now and again.
    </Text>
    <Heading>What is expected from a DTWM member?</Heading>
    <UnorderedList>
      <ListItem></ListItem>
      <ListItem>
        Interact with the community by coming to ops at least once a month or
        chatting in Discord or you will be kicked
      </ListItem>
    </UnorderedList>
    <Heading>Joining DTWM</Heading>
    <Text>
      Join our{" "}
      <Link href="https://joindtwm.vercel.app/join">
        <a>Discord server</a>
      </Link>{" "}
      and say you want to join. You'll get access to the event announcements so
      you can know when we're playing.
    </Text>
    <br />
    <Text fontSize="sm">
      You can try out our ops before joining. Ask for the Ogryn Auxilliary role.
    </Text>
  </Article>
);

export default Info;
