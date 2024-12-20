"use client";

import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { MenuIcon } from "lucide-react";

export default function SidebarTrigger() {
  const { toggleSidebar } = useSidebar();

  return (
    <Button
      variant="outline"
      size="icon"
      className="lg:hidden"
      onClick={toggleSidebar}
    >
      <MenuIcon className="h-6 w-6" />
      <span className="sr-only">Toggle navigation menu</span>
    </Button>
  );
}
