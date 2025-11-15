import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TrendingUp, TrendingDown, Phone, DollarSign, Target, Package, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const suppliers = [
  {
    id: 1,
    name: "Medisupply SAS",
    performance: 94,
    monthlySpend: 8200,
    status: "excellent",
    trend: "up",
  },
  {
    id: 2,
    name: "PharmaCore Europe",
    performance: 82,
    monthlySpend: 3100,
    status: "good",
    trend: "stable",
  },
  {
    id: 3,
    name: "BioMed Labs",
    performance: 78,
    monthlySpend: 1500,
    status: "good",
    trend: "up",
  },
  {
    id: 4,
    name: "HealthChem Imports",
    performance: 63,
    monthlySpend: 400,
    status: "warning",
    trend: "down",
  },
  {
    id: 5,
    name: "MediTech Solutions",
    performance: 88,
    monthlySpend: 5600,
    status: "excellent",
    trend: "up",
  },
  {
    id: 6,
    name: "Global Pharma Inc",
    performance: 71,
    monthlySpend: 2800,
    status: "fair",
    trend: "stable",
  },
  {
    id: 7,
    name: "EuroDrug Supply",
    performance: 85,
    monthlySpend: 4200,
    status: "good",
    trend: "up",
  },
  {
    id: 8,
    name: "QuickMed Logistics",
    performance: 67,
    monthlySpend: 1900,
    status: "warning",
    trend: "down",
  },
  {
    id: 9,
    name: "Prime Health Partners",
    performance: 92,
    monthlySpend: 6100,
    status: "excellent",
    trend: "up",
  },
];

const SuppliersROI = () => {
  const { toast } = useToast();

  const handleUpdatePrices = (supplierName: string) => {
    toast({
      title: "Update Prices",
      description: `Opening price update form for ${supplierName}`,
    });
  };

  const handleUpdateProducts = (supplierName: string) => {
    toast({
      title: "Update Products",
      description: `Opening product catalog for ${supplierName}`,
    });
  };

  const handleRemindSupplier = (supplierName: string) => {
    toast({
      title: "Follow Up ",
      description: `Sending reminder to ${supplierName}`,
    });
  };

  const totalSpend = suppliers.reduce((sum, s) => sum + s.monthlySpend, 0);
  const avgPerformance = Math.round(suppliers.reduce((sum, s) => sum + s.performance, 0) / suppliers.length);
  const excellentSuppliers = suppliers.filter((s) => s.status === "excellent").length;
  const warningSuppliers = suppliers.filter((s) => s.status === "warning").length;

  return (
    <div className="space-y-6">
      {/* Overview Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Target className="h-5 w-5 text-primary" />
            Strategic ROI Overview
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground flex items-center gap-1">
                <DollarSign className="h-4 w-4" />
                Total Monthly Spend
              </p>
              <p className="text-2xl font-bold">€{totalSpend.toLocaleString()}</p>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground flex items-center gap-1">
                <TrendingUp className="h-4 w-4" />
                Avg Performance
              </p>
              <p className="text-2xl font-bold">{avgPerformance}%</p>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground flex items-center gap-1">
                <Target className="h-4 w-4" />
                Top Performers
              </p>
              <p className="text-2xl font-bold text-green-600">{excellentSuppliers}</p>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground flex items-center gap-1">
                <AlertCircle className="h-4 w-4" />
                Needs Attention
              </p>
              <p className="text-2xl font-bold text-amber-600">{warningSuppliers}</p>
            </div>
          </div>
          <div className="mt-6 p-4 bg-muted/50 rounded-lg">
            <p className="text-sm">
              <strong>Strategic Insight:</strong> {excellentSuppliers} suppliers are performing exceptionally well,
              accounting for{" "}
              {Math.round(
                (suppliers.filter((s) => s.status === "excellent").reduce((sum, s) => sum + s.monthlySpend, 0) /
                  totalSpend) *
                  100,
              )}
              % of total spend. Consider consolidating volumes with top performers to maximize ROI.
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Suppliers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {suppliers.map((supplier) => (
          <Card key={supplier.id} className="hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <CardTitle className="text-lg">{supplier.name}</CardTitle>
                {supplier.trend === "up" && <TrendingUp className="h-4 w-4 text-green-600" />}
                {supplier.trend === "down" && <TrendingDown className="h-4 w-4 text-red-600" />}
              </div>
              <Badge
                variant={
                  supplier.status === "excellent" ? "default" : supplier.status === "good" ? "secondary" : "destructive"
                }
                className="w-fit mt-1"
              >
                {supplier.status.charAt(0).toUpperCase() + supplier.status.slice(1)}
              </Badge>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Performance</span>
                  <span className="font-semibold">{supplier.performance}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Monthly Spend</span>
                  <span className="font-semibold">€{supplier.monthlySpend.toLocaleString()}</span>
                </div>
              </div>

              <div className="flex flex-col gap-2 pt-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full"
                  onClick={() => handleUpdatePrices(supplier.name)}
                >
                  <DollarSign className="h-4 w-4 mr-2" />
                  Update Prices
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full"
                  onClick={() => handleUpdateProducts(supplier.name)}
                >
                  <Package className="h-4 w-4 mr-2" />
                  Update Products
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full"
                  onClick={() => handleRemindSupplier(supplier.name)}
                >
                  <Phone className="h-4 w-4 mr-2" />
                  Follow Up
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default SuppliersROI;
