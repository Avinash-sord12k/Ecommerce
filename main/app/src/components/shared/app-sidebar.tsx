import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { getFullUrl } from "@/lib/utils";
import { NavLinks } from "@/app/global/data";
import Link from "next/link";
import { JSX } from "react";

export function AppSidebar({
  logoText,
  LogoIcon,
}: {
  logoText: string;
  LogoIcon: JSX.ElementType;
}) {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarHeader>
            <Link
              href={getFullUrl("/")}
              className="mr-6 flex ml-4 gap-4 items-center justify-center"
              prefetch={false}
            >
              <LogoIcon className="h-6 w-6" />
              <span className="sr-only">logo</span>
              <span className="text-lg">{logoText}</span>
            </Link>
          </SidebarHeader>
          <SidebarGroupContent>
            <SidebarMenu>
              {NavLinks.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
