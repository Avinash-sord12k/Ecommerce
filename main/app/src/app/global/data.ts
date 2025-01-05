import { getFullUrl } from "@/lib/utils";
import { Home, Inbox, MountainIcon } from "lucide-react";

export const NavLinks = [
  {
    title: "Home",
    url: getFullUrl("/"),
    icon: Home,
  },
  {
    title: "All Products",
    url: getFullUrl("/products"),
    icon: Inbox,
  },
  {
    title: "Cart",
    url: getFullUrl("/checkout"),
    icon: Inbox,
  },
];

export const AppMetaData = {
  title: "Ecommerce",
  description: "Ecommerce website",
  icon: MountainIcon,
};
