import ProductGroup from "@/components/pages/home/ProductGroup";
import { operations } from "@/schema";
import { API_ENDPOINTS } from "@/store/api/config";
import { cookies } from "next/headers";
import { redirect, RedirectType } from "next/navigation";

export interface HomePageStructure {
  id: number;
  title: string;
  description: string;
  query: operations["get_products_api_v1_product_get"]["parameters"]["query"];
}

export type ProductResponse = operations["get_products_api_v1_product_get"]["responses"]["200"]["content"]["application/json"];

const pageStructure: HomePageStructure[] = [
  {
    id: 1,
    title: "Groceries",
    description: "Check out our best selling groceries",
    query: {
      category_id: 4,
      page: 1,
      page_size: 4,
    },
  },
  {
    id: 2,
    title: "Fragrances Products",
    description: "Check out our fragrances products",
    query: {
      category_id: 2,
      page: 1,
      page_size: 4,
    },
  },
  {
    id: 3,
    title: "Furniture Products",
    description: "Check out our furniture products",
    query: {
      category_id: 3,
      page: 1,
      page_size: 4,
    },
  },
];

async function getProducts(structure: HomePageStructure): Promise<ProductResponse | null> {
  const url = new URL(API_ENDPOINTS.getProducts, process.env.API_URL);

  if (structure.query) {
    Object.entries(structure.query).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        url.searchParams.append(key, String(value));
      }
    });
  }

  const cookieList = await cookies();
  const allCookie = cookieList.getAll();
  if (!allCookie?.length) {
    redirect("/login", RedirectType.replace);
  }

  const products = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      cookie: allCookie.map((cookie) => `${cookie.name}=${cookie.value}`).join("; "),
    },
  }).then((res) => {
    return res.json();
  });

  console.log("🚀 ~ getProducts ~ products:", products);
  return products;
}

export default async function Home() {
  const PageData = await Promise.all(
    pageStructure.map(async (structure) => {
      const products = await getProducts(structure);
      console.log("🚀 ~ pageStructure.map ~ products:", !!products);
      return {
        ...structure,
        ...(products && { products }),
      };
    })
  );
  console.log("🚀 ~ Home ~ PageData:", !!PageData);

  return (
    <main>
      <section className="bg-black py-32">
        <div className=" mx-auto container w-full">
          <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl text-white text-center mb-3">Spring Collection</h1>
          <p className="max-w-[600px] mx-auto text-center text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
            Introducing our vibrant and stylish spring collection. Find the perfect outfit for the season.
          </p>
        </div>
      </section>

      {PageData?.map(
        (data) =>
          data?.products && (
            <ProductGroup key={data.id} id={data.id} query={data.query} title={data.title} description={data.description} products={data?.products} />
          )
      )}
    </main>
  );
}
