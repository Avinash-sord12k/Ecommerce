import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Facebook, InstagramIcon, LinkedinIcon, TwitterIcon } from "lucide-react";
import { AppMetaData } from "@/app/global/data";
import { NavLinks } from "./app-topbar";
import { JSX } from "react";

export default function AppFooter({
  navlinks,
  LogoIcon,
  logoText,
}: {
  navlinks: NavLinks[];
  LogoIcon: JSX.ElementType;
  logoText: string;
}) {
  return (
    <>
      {/* <section className="w-full py-8 md:py-12 lg:py-16 dark:bg-zinc-900 bg-zinc-100">
        <div className="container mx-auto px-4 md:px-6 flex flex-col items-center text-center">
          <h2 className="text-2xl font-bold sm:text-3xl md:text-4xl lg:text-5xl/none dark:text-zinc-100 text-zinc-800">
            Stay Connected
          </h2>
          <p className="mx-auto max-w-[700px] dark:text-zinc-100 md:text-lg text-zinc-800">
            Subscribe to our newsletter and follow us on our social media.
          </p>
          <div className="w-full max-w-md space-y-2 my-4">
            <form className="flex space-x-2">
              <Input type="email" placeholder="Enter your email" className="max-w-lg flex-1 text-zinc-900 bg-white" />
              <Button type="submit" variant="outline">
                Subscribe
              </Button>
            </form>
          </div>
          <div className="flex justify-center space-x-4">
            <Link href="#" aria-label="Facebook page" className="text-white" prefetch={false}>
              <Facebook className="h-6 w-6" />
            </Link>
            <Link href="#" aria-label="Twitter profile" className="text-white" prefetch={false}>
              <TwitterIcon className="h-6 w-6" />
            </Link>
            <Link href="#" aria-label="Instagram profile" className="text-white" prefetch={false}>
              <InstagramIcon className="h-6 w-6" />
            </Link>
            <Link href="#" aria-label="LinkedIn profile" className="text-white" prefetch={false}>
              <LinkedinIcon className="h-6 w-6" />
            </Link>
          </div>
        </div>
      </section>
      <footer className="bg-gray-100 py-6 dark:bg-gray-800">
        <div className="container mx-auto flex items-center justify-between px-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            &copy; 2024 {AppMetaData.title}. All rights reserved.
          </p>
          <nav className="flex space-x-4">
            <Link href="#" className="text-sm hover:underline" prefetch={false}>
              Privacy
            </Link>
            <Link href="#" className="text-sm hover:underline" prefetch={false}>
              Terms
            </Link>
            <Link href="#" className="text-sm hover:underline" prefetch={false}>
              Contact
            </Link>
          </nav>
        </div>
      </footer> */}

      <footer className="bg-[#f5f5f5] py-12">
        <div className="container mx-auto px-4 lg:px-6 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="col-span-1 flex flex-col items-start lg:items-start">
              <div className="flex items-center space-x-2">
                <LogoIcon className="w-8 h-8 text-black" />
                <span className="text-lg font-bold">{logoText}</span>
              </div>
              <p className="text-gray-600 mt-2">
                Making the world a better place through constructing elegant hierarchies for maximum code reuse and
                extensibility.
              </p>
            </div>
            <div className="col-span-1 flex flex-col items-start lg:items-end" />
            <div>
              <h3 className="text-lg font-bold mb-3">Quick Links</h3>
              <ul className="space-y-2 text-gray-600">
                <li>
                  <Link href="#" prefetch={false}>
                    Home
                  </Link>
                </li>
                <li>
                  <Link href="#" prefetch={false}>
                    About Us
                  </Link>
                </li>
                <li>
                  <Link href="#" prefetch={false}>
                    Services
                  </Link>
                </li>
                <li>
                  <Link href="#" prefetch={false}>
                    Contact
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-bold mb-3">Legal</h3>
              <ul className="space-y-2 text-gray-600">
                <li>
                  <Link href="#" prefetch={false}>
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link href="#" prefetch={false}>
                    Terms of Service
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <hr className="mt-8" />
          <div className="flex items-center justify-between mt-8">
            <div className=" space-y-2">
              <div className="flex items-center space-x-2">
                <LogoIcon className="w-6 h-6 text-black" />
                <span className="text-lg font-bold">{logoText}</span>
              </div>
              <p>
                &copy; {new Date().getFullYear()} {AppMetaData.title}. All rights reserved.
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="link">Facebook</Button>
              <Button variant="link">Twitter</Button>
              <Button variant="link">Instagram</Button>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
}
