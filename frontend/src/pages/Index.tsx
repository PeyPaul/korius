import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import ControlTower from "@/components/tabs/ControlTower";
import InventoryOrders from "@/components/tabs/InventoryOrders";
import SuppliersROI from "@/components/tabs/SuppliersROI";
import AISuggestions from "@/components/AISuggestions";
import { TowerControl, Package, Building2 } from "lucide-react";
import { cn } from "@/lib/utils";

const Index = () => {
  const [activeTab, setActiveTab] = useState("control-tower");

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-foreground">Korius</h1>
              <p className="text-sm text-muted-foreground">AI-Powered Procurement Automation</p>
            </div>
            <nav className="flex items-center gap-1">
              <button
                onClick={() => setActiveTab("control-tower")}
                className={cn(
                  "px-4 py-2 text-sm font-medium rounded-md transition-colors",
                  activeTab === "control-tower"
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent",
                )}
              >
                Control Center
              </button>

              <button
                onClick={() => setActiveTab("suppliers")}
                className={cn(
                  "px-4 py-2 text-sm font-medium rounded-md transition-colors",
                  activeTab === "suppliers"
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent",
                )}
              >
                Suppliers
              </button>

              <button
                onClick={() => setActiveTab("inventory")}
                className={cn(
                  "px-4 py-2 text-sm font-medium rounded-md transition-colors",
                  activeTab === "inventory"
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent",
                )}
              >
                Products
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_380px] gap-6">
          {/* Main Content Area */}
          <div>
            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsContent value="control-tower" className="space-y-6">
                <ControlTower />
              </TabsContent>

              <TabsContent value="inventory" className="space-y-6">
                <InventoryOrders />
              </TabsContent>

              <TabsContent value="suppliers" className="space-y-6">
                <SuppliersROI />
              </TabsContent>
            </Tabs>
          </div>

          {/* Suggestions Sidebar */}
          <div className="hidden lg:block">
            <AISuggestions activeTab={activeTab} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
