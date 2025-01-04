import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "../ui/badge";
import { components } from "@/schema";
import Link from "next/link";
import { calculateDiscountPercent, cutWords } from "@/lib/utils";

type ProductCardProps = components["schemas"]["PaginatedResponse_ProductResponseModel_"]["items"][0] & {};

const ProductCard = ({ id, name, description, price, discount, images, thumbnail }: ProductCardProps) => {
  const discountPercent = calculateDiscountPercent(Number(price), Number(discount));

  // Calculate delay dynamically based on the staggerIndex

  return (
    <Link href={`/products/${id}`}>
      <Card
        className="shadow-none animate-in fade-in duration-300"
        style={{}} // Apply the staggered delay dynamically
      >
        <CardHeader>
          {<img src={thumbnail ?? images?.[0] ?? "/images/vase_cropped.jpg"} alt="Product" className="rounded-lg" />}
        </CardHeader>
        <CardContent>
          <CardTitle className="text-lg font-bold">{name}</CardTitle>
          <CardDescription className="text-sm text-gray-500">{cutWords(description ?? "", 20)}</CardDescription>
          <div className="flex items-center justify-between mt-4">
            <div>
              <span className="text-xl font-semibold text-green-600">
                {Number(price)?.toLocaleString("en-IN", {
                  currency: "INR",
                  currencyDisplay: "narrowSymbol",
                  style: "currency",
                  currencySign: "accounting",
                  maximumFractionDigits: 0,
                  maximumSignificantDigits: 1,
                })}
              </span>
              <span className="text-sm text-gray-500 line-through ml-2">
                {Number(discount)?.toLocaleString("en-IN", {
                  currency: "INR",
                  currencyDisplay: "narrowSymbol",
                  style: "currency",
                  currencySign: "accounting",
                  maximumFractionDigits: 0,
                  maximumSignificantDigits: 1,
                })}
              </span>
            </div>
            {discountPercent >= 1 && <Badge className="bg-red-500 text-white px-2 py-1">{discountPercent}% OFF</Badge>}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
};

export default ProductCard;
