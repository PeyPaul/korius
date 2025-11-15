import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Lightbulb, TrendingUp, AlertTriangle, DollarSign, Package, Users } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface AISuggestionsProps {
  activeTab: string;
}

const AISuggestions = ({ activeTab }: AISuggestionsProps) => {
  const { toast } = useToast();

  const handleApplySuggestion = (suggestion: string) => {
    toast({
      title: "Applying Suggestion",
      description: `Implementing: ${suggestion}`,
    });
  };

  const controlTowerSuggestions = [
    {
      icon: DollarSign,
      badge: "Cost Saving",
      badgeColor: "bg-success/10 text-success border-success/20",
      iconBg: "bg-success/10",
      iconColor: "text-success",
      amount: "€2,400/year",
      text: "Switch Ibuprofen supplier to MediSupply for 18% cost reduction",
      action: "Apply",
      actionVariant: "default" as const,
      suggestion: "Switch Ibuprofen supplier",
    },
    {
      icon: AlertTriangle,
      badge: "Risk Alert",
      badgeColor: "bg-critical/10 text-critical border-critical/20",
      iconBg: "bg-critical/10",
      iconColor: "text-critical",
      text: "HealthChem Imports reliability dropped 23% - consider alternatives",
      action: "Review",
      actionVariant: "outline" as const,
      suggestion: "Review HealthChem alternatives",
    },
    {
      icon: TrendingUp,
      badge: "Optimization",
      badgeColor: "bg-primary/10 text-primary border-primary/20",
      iconBg: "bg-primary/10",
      iconColor: "text-primary",
      amount: "€1,200/year",
      text: "Bulk order Paracetamol quarterly instead of monthly for better pricing",
      action: "Optimize",
      actionVariant: "outline" as const,
      suggestion: "Adjust Paracetamol ordering",
    },
    {
      icon: TrendingUp,
      badge: "New Product",
      badgeColor: "bg-moderate/10 text-moderate border-moderate/20",
      iconBg: "bg-moderate/10",
      iconColor: "text-moderate",
      text: "New generic Amoxicillin available from BioMed Labs at 15% lower cost",
      action: "Explore",
      actionVariant: "outline" as const,
      suggestion: "Explore new Amoxicillin option",
    },
  ];

  const inventorySuggestions = [
    {
      icon: Package,
      badge: "Stock Alert",
      badgeColor: "bg-critical/10 text-critical border-critical/20",
      iconBg: "bg-critical/10",
      iconColor: "text-critical",
      text: "Aspirin stock will run out in 3 days - reorder immediately",
      action: "Order Now",
      actionVariant: "default" as const,
      suggestion: "Reorder Aspirin",
    },
    {
      icon: TrendingUp,
      badge: "Forecast",
      badgeColor: "bg-primary/10 text-primary border-primary/20",
      iconBg: "bg-primary/10",
      iconColor: "text-primary",
      text: "Seasonal flu medication demand expected to increase 35% next month",
      action: "Adjust",
      actionVariant: "outline" as const,
      suggestion: "Increase flu medication stock",
    },
    {
      icon: DollarSign,
      badge: "Overstock",
      badgeColor: "bg-moderate/10 text-moderate border-moderate/20",
      iconBg: "bg-moderate/10",
      iconColor: "text-moderate",
      amount: "€800 tied up",
      text: "Vitamin D surplus - reduce next order by 40%",
      action: "Adjust",
      actionVariant: "outline" as const,
      suggestion: "Reduce Vitamin D order",
    },
    {
      icon: AlertTriangle,
      badge: "Expiry Warning",
      badgeColor: "bg-critical/10 text-critical border-critical/20",
      iconBg: "bg-critical/10",
      iconColor: "text-critical",
      text: "12 items expiring within 30 days - promote or return to supplier",
      action: "Review",
      actionVariant: "outline" as const,
      suggestion: "Handle expiring items",
    },
  ];

  const suppliersSuggestions = [
    {
      icon: Users,
      badge: "Performance",
      badgeColor: "bg-success/10 text-success border-success/20",
      iconBg: "bg-success/10",
      iconColor: "text-success",
      text: "PharmaDirect consistently delivers 2 days early - negotiate volume discount",
      action: "Contact",
      actionVariant: "default" as const,
      suggestion: "Negotiate with PharmaDirect",
    },
    {
      icon: AlertTriangle,
      badge: "Risk Alert",
      badgeColor: "bg-critical/10 text-critical border-critical/20",
      iconBg: "bg-critical/10",
      iconColor: "text-critical",
      text: "MedSource late on 60% of deliveries last month - find backup supplier",
      action: "Review",
      actionVariant: "outline" as const,
      suggestion: "Find MedSource alternative",
    },
    {
      icon: DollarSign,
      badge: "ROI Opportunity",
      badgeColor: "bg-primary/10 text-primary border-primary/20",
      iconBg: "bg-primary/10",
      iconColor: "text-primary",
      amount: "€3,200/year",
      text: "Consolidate orders with GlobalMeds for tiered pricing benefits",
      action: "Calculate",
      actionVariant: "outline" as const,
      suggestion: "Consolidate GlobalMeds orders",
    },
    {
      icon: TrendingUp,
      badge: "New Supplier",
      badgeColor: "bg-moderate/10 text-moderate border-moderate/20",
      iconBg: "bg-moderate/10",
      iconColor: "text-moderate",
      text: "EuroPharma offering 20% discount for first 3 months - certified supplier",
      action: "Explore",
      actionVariant: "outline" as const,
      suggestion: "Evaluate EuroPharma offer",
    },
  ];

  const currentSuggestions =
    activeTab === "control-tower"
      ? controlTowerSuggestions
      : activeTab === "inventory"
        ? inventorySuggestions
        : suppliersSuggestions;

  return (
    <Card className="p-6 sticky top-24 h-fit">
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="h-5 w-5 text-primary" />
        <h3 className="font-semibold text-lg text-foreground">Recommendations</h3>
      </div>

      <div className="space-y-4">
        {currentSuggestions.map((item, index) => (
          <div key={index} className="p-4 border border-border rounded-lg bg-card hover:shadow-md transition-shadow">
            <div className="flex items-start gap-3">
              <div className={`p-2 ${item.iconBg} rounded-lg`}>
                <item.icon className={`h-4 w-4 ${item.iconColor}`} />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant="outline" className={item.badgeColor}>
                    {item.badge}
                  </Badge>
                  {item.amount && <span className="text-xs text-muted-foreground">{item.amount}</span>}
                </div>
                <p className="text-sm text-foreground mb-2">{item.text}</p>
                <Button
                  size="sm"
                  variant={item.actionVariant}
                  onClick={() => handleApplySuggestion(item.suggestion)}
                  className="w-full"
                >
                  {item.action}
                </Button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default AISuggestions;
