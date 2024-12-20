import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import Link from "next/link"
import { JSX } from "react"

export interface NavLinks {
  title: string
  href: string
}

export default function Topbar({navlinks, LogoIcon, logoText}: {navlinks: NavLinks[], LogoIcon: JSX.ElementType, logoText: string}) {
  const rootPath = process.env.NEXT_PUBLIC_BASE_PATH || ""
  return (
    <header className="flex h-20 w-full shrink-0 items-center px-4 md:px-6 border-b ">
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="outline" size="icon" className="lg:hidden">
            <MenuIcon className="h-6 w-6" />
            <span className="sr-only">Toggle navigation menu</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="left">
            <SheetTitle>Menu</SheetTitle>
          <Link href={`${rootPath}/`} className="mr-6 hidden lg:flex" prefetch={false}>
            <LogoIcon className="h-6 w-6" />
            <span className="sr-only">{logoText}</span>
          </Link>
          <div className="grid gap-2 py-6">
            {navlinks.map((link, index) => (
              <Link key={index} href={link.href} className="flex w-full items-center py-2 text-lg font-semibold" prefetch={false}>
                <Button variant={"ghost"} className="">
                  {link.title}
                </Button>
            </Link>
            ))}
          </div>
        </SheetContent>
      </Sheet>
      <Link href={`${rootPath}/`} className="mr-6 hidden lg:flex" prefetch={false}>
        <LogoIcon className="h-6 w-6" />
        <span className="sr-only">{logoText}</span>
      </Link>
      <nav className="ml-auto hidden lg:flex gap-6">
        {navlinks.map((link, index) => (
          <Link
          href={link.href}
          key={index}
          prefetch={false}
        >
          <Button variant={"ghost"}>
            {link.title}
          </Button>
        </Link>
        ))}
      </nav>
    </header>
  )
}

function MenuIcon(props: {[key: string]: string}) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="4" x2="20" y1="12" y2="12" />
      <line x1="4" x2="20" y1="6" y2="6" />
      <line x1="4" x2="20" y1="18" y2="18" />
    </svg>
  )
}