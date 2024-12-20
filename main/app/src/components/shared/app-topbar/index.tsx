import { getFullUrl } from "@/lib/utils";
import Link from "next/link";
import { JSX } from "react";
import SidebarTrigger from "./SidebarTrigger";

export interface NavLinks {
  title: string;
  url: string;
  icon: JSX.ElementType;
}

export default function Topbar({
  navlinks,
  LogoIcon,
  logoText,
}: {
  navlinks: NavLinks[];
  LogoIcon: JSX.ElementType;
  logoText: string;
}) {
  return (
    <header className=" border-b ">
      <div className=" container mx-auto flex h-14 w-full shrink-0 items-center px-4 md:px-6">
        <Link
          href={getFullUrl("/")}
          className="mr-6 flex ml-4 gap-4 items-center justify-center"
          prefetch={false}
        >
          <LogoIcon className="h-6 w-6" />
          <span className="sr-only">{logoText}</span>
          <span className="text-lg">{logoText}</span>
        </Link>
        <nav className="ml-auto hidden md:flex gap-6">
          {navlinks.map((link, index) => (
            <Link key={index} href={getFullUrl(link.url)} prefetch={false}>
              {link.title}
            </Link>
          ))}
        </nav>
        <div className="block md:hidden ml-auto">
          <SidebarTrigger />
        </div>
      </div>
    </header>
  );
}
