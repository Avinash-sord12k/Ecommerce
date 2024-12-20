import Topbar from "@/components/ui/Topbar";
import { MountainIcon } from "lucide-react";

const navlinks = [
  { title: "Home", href: `${process.env.NEXT_PUBLIC_BASE_PATH}/` },
  { title: "About", href: `${process.env.NEXT_PUBLIC_BASE_PATH}/about` },
  { title: "Services", href: `${process.env.NEXT_PUBLIC_BASE_PATH}/services` },
]

export default function Home() {
  return (
    <div className="">
      <Topbar
         navlinks={navlinks}
         LogoIcon={MountainIcon}
         logoText="Logo"
      />
    </div>
  );
}
