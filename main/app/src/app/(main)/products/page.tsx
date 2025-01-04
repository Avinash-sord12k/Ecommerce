import { Input } from "@/components/ui/input";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "@/components/ui/accordion";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ArrowUpDownIcon, SearchIcon } from "lucide-react";

export default function AllProducts() {
  return (
    <section className="container mx-auto p-6">
      <div className="flex items-center mb-8">
        <div className="relative w-full">
          <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500" />
          <Input className="pl-10 pr-4 py-2 rounded-lg w-full" type="search" placeholder="Search for products..." />
        </div>
      </div>
      <div className="grid lg:grid-cols-4 gap-6">
        <aside className="lg:col-span-1">
          <div className="mb-6">
            <h2 className="font-semibold mb-2">Filters</h2>
            <div className="space-y-4">
              <Accordion type="single" collapsible className="w-full">
                <AccordionItem value="category">
                  <AccordionTrigger className="text-base">Category</AccordionTrigger>
                  <AccordionContent>
                    <div className="grid gap-2">
                      <Label className="flex items-center gap-2 font-normal">
                        <Checkbox id="category-electronics" /> Electronics
                      </Label>
                      <Label className="flex items-center gap-2 font-normal">
                        <Checkbox id="category-books" /> Books
                      </Label>
                      <Label className="flex items-center gap-2 font-normal">
                        <Checkbox id="category-clothing" /> Clothing
                      </Label>
                    </div>
                  </AccordionContent>
                </AccordionItem>
                <AccordionItem value="price">
                  <AccordionTrigger className="text-base">Price</AccordionTrigger>
                  <AccordionContent>
                    <div className="grid gap-2">
                      <Label className="flex items-center gap-2 font-normal">
                        <Checkbox id="price-under-25" /> Under $25
                      </Label>
                      <Label className="flex items-center gap-2 font-normal">
                        <Checkbox id="price-25-to-50" /> $25 to $50
                      </Label>
                      <Label className="flex items-center gap-2 font-normal">
                        <Checkbox id="price-over-50" /> Over $50
                      </Label>
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </div>
          </div>
        </aside>
        <div className="lg:col-span-3">
          <div className="flex justify-end mb-6">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="ml-auto shrink-0">
                  <ArrowUpDownIcon className="w-4 h-4 mr-2" />
                  Sort by
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-[200px]" align="end">
                <DropdownMenuRadioGroup value="featured">
                  <DropdownMenuRadioItem value="featured">Featured</DropdownMenuRadioItem>
                  <DropdownMenuRadioItem value="popular">Most Popular</DropdownMenuRadioItem>
                  <DropdownMenuRadioItem value="new">Newest Arrivals</DropdownMenuRadioItem>
                  <DropdownMenuRadioItem value="low-to-high">Price: Low to High</DropdownMenuRadioItem>
                  <DropdownMenuRadioItem value="high-to-low">Price: High to Low</DropdownMenuRadioItem>
                </DropdownMenuRadioGroup>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, idx) => (
              <div key={idx} className="relative group">
                <Link href="#" className="absolute inset-0 z-10" prefetch={false}>
                  <span className="sr-only">View Product</span>
                </Link>
                <img
                  src="/images/vase_cropped.jpg"
                  alt="Product image"
                  width={200}
                  height={200}
                  className="rounded-lg object-cover w-full aspect-square group-hover:opacity-50 transition-opacity"
                />
                <div className="py-4">
                  <h3 className="font-semibold tracking-tight">Product Name</h3>
                  <p className="text-sm leading-none text-gray-500">Product Description</p>
                  <h4 className="font-semibold">$99.99</h4>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
