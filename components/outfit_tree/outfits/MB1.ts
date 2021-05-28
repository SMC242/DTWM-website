import { TreeNode } from "../create_amchart";

// TODO: move this to the API
const MB1: TreeNode = {
  name: "unknown",
  tag: "MB1",
  faction: "NC",
  children: [
    { name: "Catharsis", tag: "CATH", faction: "NC", circumstances: "split" },
    {
      name: "Main Battalion",
      tag: "MBn",
      faction: "NC",
      circumstances: "split",
      children: [
        {
          name: "Siege Unit",
          tag: "SIGE",
          faction: "NC",
          circumstances: "split",
          children: [
            {
              name: "Friendly Fire Force",
              tag: "4RCE",
              faction: "NC",
              circumstances: "split",
            },
          ],
        },
        {
          name: "The Origin",
          tag: "ORlG",
          faction: "NC",
          circumstances: "split",
          id: "ORlG",
          children: [
            {
              name: "Nomad Predators",
              tag: "N0PR",
              faction: "NC",
              circumstances: "split",
              id: "N0PR 2",
            },
          ],
        },
        {
          name: "NC Legionaires",
          tag: "L3GN",
          faction: "NC",
          circumstances: "split",
          children: [
            {
              name: "Sanctuary (skillfit)",
              tag: "S4Y",
              faction: "NC",
              id: "S4Y 1",
              circumstances: "split",
              children: [
                {
                  name: "Sactuary (midfit)",
                  tag: "S4Y",
                  faction: "NC",
                  circumstances: "split",
                  id: "S4Y 2",
                  children: [
                    {
                      name: "Nomand Predators",
                      tag: "N0PR",
                      faction: "NC",
                      circumstances: "split",
                      id: "N0PR 1",
                      links: ["ORlG"],
                    },
                  ],
                },
              ],
            },
            {
              name: "Deathwatch Marines (Cobalt)",
              tag: "DTWM",
              faction: "NC",
              circumstances: "split",
              id: "DTWM 1",
              children: [
                {
                  name: "Federation of Pog Champ",
                  tag: "POGS",
                  faction: "NC",
                  circumstances: "split",
                  links: ["DTWM 2"],
                },
                {
                  name: "Deathwatch Marines (Miller)",
                  tag: "DTWM",
                  faction: "NC",
                  circumstances: "reformed",
                  id: "DTWM 2",
                  children: [
                    {
                      name: "Baby Sharks",
                      tag: "d0d0",
                      faction: "VS",
                      circumstances: "split",
                      links: ["DTWM 2"],
                    },
                  ],
                },
              ],
            },
            {
              name: "Members of The Utopian Mummys",
              tag: "MUMS",
              faction: "VS",
              circumstances: "split",
              children: [
                {
                  name: "Urge To Confess",
                  tag: "URGE",
                  faction: "VS",
                  circumstances: "split",
                  children: [
                    {
                      name: "One Man Cringe Army",
                      tag: "1KPM",
                      faction: "TR",
                      circumstances: "split",
                    },
                    {
                      name: "The Wyverns",
                      tag: "WVRN",
                      faction: "VS",
                      circumstances: "split",
                    },
                    {
                      name: "Yet Another Cobalt Outfit",
                      tag: "YACO",
                      faction: "VS",
                      circumstances: "split",
                    },
                  ],
                },
                {
                  name: "Members of The Ultimate Mummys",
                  tag: "MUMS",
                  faction: "NC",
                  circumstances: "reformed",
                  children: [
                    {
                      name: "Oops We Did It Again",
                      tag: "OOP5",
                      faction: "NC",
                      circumstances: "split",
                    },
                  ],
                },
              ],
            },
            {
              name: "Terran Night Watch",
              tag: "TRNW",
              faction: "TR",
              circumstances: "split",
              children: [
                {
                  name: "Talon Comp",
                  tag: "T4NC",
                  faction: "NC",
                  circumstances: "reformed",
                  children: [
                    {
                      name: "Auraxium Marines",
                      tag: "AXMI",
                      faction: "NC",
                      circumstances: "merge",
                      children: [
                        {
                          name: "Nova Tactical",
                          tag: "TAN0",
                          faction: "NC",
                          circumstances: "split",
                          links: ["TPDV"],
                        },
                        {
                          name: "The Phantom Devious",
                          tag: "TPDV",
                          faction: "NC",
                          circumstances: "split",
                        },
                      ],
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
  ],
};
export default MB1;
