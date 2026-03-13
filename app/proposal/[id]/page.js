'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams } from 'next/navigation';
import { Check, MessageCircle, Download, Link2, ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export default function ProposalPage() {
  const params = useParams();
  const [proposal, setProposal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [exporting, setExporting] = useState(false);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const contentRef = useRef(null);
  const carouselRef = useRef(null);

  useEffect(() => {
    if (params?.id) {
      fetchProposal();
    }
  }, [params?.id]);

  // Auto-scroll carousel
  useEffect(() => {
    if (proposal?.carouselCreatives?.length > 3) {
      const interval = setInterval(() => {
        setCurrentSlide((prev) => {
          const maxSlide = proposal.carouselCreatives.length - 3;
          return prev >= maxSlide ? 0 : prev + 1;
        });
      }, 3000); // Change every 3 seconds

      return () => clearInterval(interval);
    }
  }, [proposal?.carouselCreatives?.length]);

  const fetchProposal = async () => {
    try {
      const response = await fetch(`/api/proposals/${params.id}`);
      const data = await response.json();
      setProposal(data.proposal);
    } catch (error) {
      console.error('Error fetching proposal:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyLink = () => {
    const url = window.location.href;
    navigator.clipboard.writeText(url);
    alert('Link copiado para a área de transferência!');
  };

  const handleExportPDF = async () => {
    if (!contentRef.current) return;
    
    setExporting(true);
    try {
      const element = contentRef.current;
      
      // Capture the entire page with proper settings
      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        logging: false,
        backgroundColor: '#000000',
        windowWidth: 1920,
        windowHeight: element.scrollHeight,
      });

      const imgData = canvas.toDataURL('image/png');
      
      // Create PDF
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'px',
        format: 'a4',
      });

      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = canvas.width;
      const imgHeight = canvas.height;
      
      // Calculate how many pages we need
      const ratio = pdfWidth / imgWidth;
      const scaledHeight = imgHeight * ratio;
      const totalPages = Math.ceil(scaledHeight / pdfHeight);
      
      // Add pages
      for (let i = 0; i < totalPages; i++) {
        if (i > 0) pdf.addPage();
        
        const position = -i * pdfHeight;
        pdf.addImage(imgData, 'PNG', 0, position, pdfWidth, scaledHeight);
      }

      pdf.save(`proposta-${proposal.companyName}.pdf`);
    } catch (error) {
      console.error('Error exporting PDF:', error);
      alert('Erro ao exportar PDF. Tente novamente.');
    } finally {
      setExporting(false);
    }
  };

  const handleWhatsApp = () => {
    const message = `Olá! Gostaria de conversar sobre a proposta: ${proposal.title}`;
    const phone = proposal.contactWhatsApp?.replace(/\D/g, '') || '';
    window.open(`https://wa.me/${phone}?text=${encodeURIComponent(message)}`, '_blank');
  };

  const handleAcceptProposal = () => {
    const planParam = selectedPlan ? `?plan=${encodeURIComponent(selectedPlan.name)}` : '';
    window.location.href = `/proposal/${params.id}/obrigado${planParam}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-lime-400"></div>
      </div>
    );
  }

  if (!proposal) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-2">Proposta não encontrada</h1>
          <p className="text-zinc-400">A proposta que você está procurando não existe.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-zinc-950 to-black">
      {/* Fixed Action Bar */}
      <div className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-b border-zinc-800">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <div className="text-white font-semibold">{proposal.companyName}</div>
          <div className="flex gap-2">
            <Button
              onClick={handleCopyLink}
              variant="outline"
              size="sm"
              className="border-zinc-700 text-zinc-300 hover:bg-zinc-800"
            >
              <Link2 className="w-4 h-4 mr-2" />
              Copiar Link
            </Button>
            <Button
              onClick={handleExportPDF}
              disabled={exporting}
              className="bg-lime-400 hover:bg-lime-500 text-black font-semibold"
              size="sm"
            >
              <Download className="w-4 h-4 mr-2" />
              {exporting ? 'Exportando...' : 'Exportar PDF'}
            </Button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div ref={contentRef} className="pt-16">
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          {proposal.coverImage && (
            <div className="absolute inset-0 opacity-20">
              <img
                src={proposal.coverImage}
                alt="Cover"
                className="w-full h-full object-cover"
              />
            </div>
          )}
          <div className="relative container mx-auto px-4 py-20 md:py-32">
            <div className="max-w-4xl mx-auto text-center">
              {proposal.clientLogo && (
                <img
                  src={proposal.clientLogo}
                  alt={proposal.companyName}
                  className="w-24 h-24 object-contain mx-auto mb-8"
                />
              )}
              <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
                {proposal.title}
              </h1>
              <p className="text-xl text-zinc-300 max-w-2xl mx-auto">
                {proposal.description}
              </p>
              <div className="mt-8 inline-flex items-center gap-2 bg-lime-400/10 border border-lime-400/30 rounded-full px-6 py-3">
                <span className="text-lime-400 font-semibold">Para:</span>
                <span className="text-white font-bold">{proposal.companyName}</span>
              </div>
            </div>
          </div>
        </section>

        {/* Strategy Overview Section */}
        {proposal.strategyOverview && (
          <section className="py-16 bg-zinc-900/30">
            <div className="container mx-auto px-4">
              <div className="max-w-4xl mx-auto">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-8 text-center">
                  Visão Geral da <span className="text-lime-400">Estratégia</span>
                </h2>
                <Card className="bg-zinc-900/50 border-zinc-800 p-8">
                  <p className="text-zinc-300 text-lg leading-relaxed whitespace-pre-wrap">
                    {proposal.strategyOverview}
                  </p>
                </Card>
              </div>
            </div>
          </section>
        )}

        {/* Pricing Plans Section */}
        {proposal.plans && proposal.plans.length > 0 && (
          <section className="py-16">
            <div className="container mx-auto px-4">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-4 text-center">
                Planos de <span className="text-lime-400">Serviço</span>
              </h2>
              <p className="text-zinc-400 text-center mb-12">Clique no plano para selecioná-lo</p>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                {proposal.plans.map((plan, index) => (
                  <Card
                    key={index}
                    onClick={() => setSelectedPlan(plan)}
                    className={`bg-zinc-900/50 border-2 cursor-pointer transition-all duration-300 p-8 relative overflow-hidden group ${
                      selectedPlan?.name === plan.name
                        ? 'border-lime-400 scale-105 shadow-xl shadow-lime-400/30 ring-4 ring-lime-400/20'
                        : index === 1
                        ? 'border-lime-400 scale-105 shadow-xl shadow-lime-400/20'
                        : 'border-zinc-800 hover:border-lime-400/50'
                    }`}
                  >
                    {selectedPlan?.name === plan.name && (
                      <div className="absolute top-0 left-0 bg-lime-400 text-black text-xs font-bold px-4 py-1 rounded-br-lg flex items-center gap-1">
                        <Check className="w-3 h-3" />
                        SELECIONADO
                      </div>
                    )}
                    {index === 1 && selectedPlan?.name !== plan.name && (
                      <div className="absolute top-0 right-0 bg-lime-400 text-black text-xs font-bold px-4 py-1 rounded-bl-lg">
                        POPULAR
                      </div>
                    )}
                    <h3 className="text-2xl font-bold text-white mb-4">{plan.name}</h3>
                    <div className="mb-6">
                      <span className="text-4xl font-bold text-lime-400">{plan.price}</span>
                      <span className="text-zinc-400 ml-2">/ mês</span>
                    </div>
                    <ul className="space-y-3 mb-8">
                      {plan.features?.map((feature, idx) => (
                        <li key={idx} className="flex items-start gap-3 text-zinc-300">
                          <Check className="w-5 h-5 text-lime-400 mt-0.5 flex-shrink-0" />
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                    {selectedPlan?.name === plan.name && (
                      <div className="mt-4 pt-4 border-t border-lime-400/30">
                        <p className="text-lime-400 text-sm font-semibold text-center">
                          ✓ Clique em "Aceitar Proposta" para continuar
                        </p>
                      </div>
                    )}
                  </Card>
                ))}
              </div>
            </div>
          </section>
        )}

        {/* Preview/Mockup Section */}
        {proposal.previewImage && (
          <section className="py-16 bg-zinc-900/30">
            <div className="container mx-auto px-4">
              <div className="max-w-4xl mx-auto">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-8 text-center">
                  Prévia <span className="text-lime-400">Visual</span>
                </h2>
                <div className="rounded-xl overflow-hidden border border-zinc-800 shadow-2xl">
                  <img
                    src={proposal.previewImage}
                    alt="Preview"
                    className="w-full h-auto"
                  />
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Creatives Gallery Section */}
        {(proposal.mainCreative || (proposal.carouselCreatives && proposal.carouselCreatives.length > 0)) && (
          <section className="py-16">
            <div className="container mx-auto px-4">
              <h2 className="text-3xl md:text-4xl font-bold text-white mb-12 text-center">
                Nossos <span className="text-lime-400">Criativos</span>
              </h2>
              
              <div className="max-w-7xl mx-auto">
                {/* Main Creative + Carousel Layout */}
                <div className="flex flex-col lg:flex-row gap-6 items-start">
                  
                  {/* Main Creative - Slightly Larger (52%) */}
                  {proposal.mainCreative && (
                    <div className="w-full lg:w-[52%] flex-shrink-0">
                      <div className="sticky top-24">
                        <div className="relative aspect-[4/5] rounded-xl overflow-hidden border-4 border-lime-400 shadow-2xl shadow-lime-400/20">
                          <img
                            src={proposal.mainCreative}
                            alt="Criativo Principal"
                            className="w-full h-full object-cover"
                          />
                          <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-6">
                            <div className="inline-block bg-lime-400 text-black px-4 py-2 rounded-full text-sm font-bold">
                              Criativo do Cliente
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Carousel - Similar Size (48%) */}
                  {proposal.carouselCreatives && proposal.carouselCreatives.length > 0 && (
                    <div className="w-full lg:w-[48%] flex-1">
                      <div className="mb-6 text-center lg:text-left">
                        <h3 className="text-lg font-semibold text-white mb-1">
                          Exemplos de Trabalhos
                        </h3>
                        <p className="text-zinc-400 text-xs">
                          Criativos de outros clientes
                        </p>
                      </div>
                      
                      <div className="relative">
                        {/* Carousel Container */}
                        <div className="overflow-hidden rounded-lg">
                          <div
                            ref={carouselRef}
                            className="flex transition-transform duration-500 ease-in-out gap-2"
                            style={{
                              transform: `translateX(-${currentSlide * 33.33}%)`,
                            }}
                          >
                            {proposal.carouselCreatives.map((creative, index) => (
                              <div
                                key={index}
                                className="w-[calc(33.33%-0.5rem)] flex-shrink-0"
                              >
                                <div className="aspect-[4/5] rounded-lg overflow-hidden border-2 border-zinc-800 hover:border-lime-400/50 transition-all shadow-lg">
                                  <img
                                    src={creative}
                                    alt={`Exemplo ${index + 1}`}
                                    className="w-full h-full object-cover"
                                  />
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* Navigation Buttons */}
                        {proposal.carouselCreatives.length > 3 && (
                          <>
                            <button
                              onClick={() =>
                                setCurrentSlide((prev) =>
                                  prev === 0 ? proposal.carouselCreatives.length - 3 : prev - 1
                                )
                              }
                              className="absolute -left-3 top-1/2 -translate-y-1/2 bg-lime-400 hover:bg-lime-500 text-black p-1.5 rounded-full shadow-lg z-10"
                            >
                              <ChevronLeft className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() =>
                                setCurrentSlide((prev) =>
                                  prev >= proposal.carouselCreatives.length - 3 ? 0 : prev + 1
                                )
                              }
                              className="absolute -right-3 top-1/2 -translate-y-1/2 bg-lime-400 hover:bg-lime-500 text-black p-1.5 rounded-full shadow-lg z-10"
                            >
                              <ChevronRight className="w-4 h-4" />
                            </button>
                          </>
                        )}

                        {/* Dots Indicator */}
                        {proposal.carouselCreatives.length > 3 && (
                          <div className="flex justify-center gap-1.5 mt-4">
                            {Array.from({
                              length: proposal.carouselCreatives.length - 2,
                            }).map((_, index) => (
                              <button
                                key={index}
                                onClick={() => setCurrentSlide(index)}
                                className={`h-1.5 rounded-full transition-all ${
                                  currentSlide === index
                                    ? 'bg-lime-400 w-6'
                                    : 'bg-zinc-600 hover:bg-zinc-500 w-1.5'
                                }`}
                              />
                            ))}
                          </div>
                        )}
                      </div>

                      {/* Grid view for 3 or less items */}
                      {proposal.carouselCreatives.length <= 3 && (
                        <div className="grid grid-cols-3 gap-2">
                          {proposal.carouselCreatives.map((creative, index) => (
                            <div
                              key={index}
                              className="aspect-[4/5] rounded-lg overflow-hidden border-2 border-zinc-800 hover:border-lime-400/50 transition-all shadow-lg"
                            >
                              <img
                                src={creative}
                                alt={`Exemplo ${index + 1}`}
                                className="w-full h-full object-cover"
                              />
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Expected Results Section */}
        {proposal.expectedResults && (
          <section className="py-16">
            <div className="container mx-auto px-4">
              <div className="max-w-4xl mx-auto">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-8 text-center">
                  Resultados <span className="text-lime-400">Esperados</span>
                </h2>
                <Card className="bg-zinc-900/50 border-zinc-800 p-8">
                  <p className="text-zinc-300 text-lg leading-relaxed whitespace-pre-wrap">
                    {proposal.expectedResults}
                  </p>
                </Card>
              </div>
            </div>
          </section>
        )}

        {/* Custom Notes Section */}
        {proposal.customNotes && (
          <section className="py-16 bg-zinc-900/30">
            <div className="container mx-auto px-4">
              <div className="max-w-4xl mx-auto">
                <Card className="bg-lime-400/10 border-lime-400/30 p-8">
                  <p className="text-zinc-200 text-lg leading-relaxed whitespace-pre-wrap">
                    {proposal.customNotes}
                  </p>
                </Card>
              </div>
            </div>
          </section>
        )}

        {/* CTA Section */}
        <section className="py-20 bg-gradient-to-b from-zinc-900/50 to-black">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
                Vamos <span className="text-lime-400">Começar?</span>
              </h2>
              <p className="text-xl text-zinc-300 mb-4">
                Estamos prontos para transformar sua presença digital
              </p>
              {selectedPlan && (
                <div className="mb-6 inline-flex items-center gap-2 bg-lime-400/10 border border-lime-400/30 rounded-full px-6 py-3">
                  <Check className="w-5 h-5 text-lime-400" />
                  <span className="text-white font-semibold">Plano selecionado: {selectedPlan.name}</span>
                </div>
              )}
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button
                  onClick={handleWhatsApp}
                  size="lg"
                  variant="outline"
                  className="border-lime-400 text-lime-400 hover:bg-lime-400/10 font-bold text-lg px-8 py-6"
                >
                  <MessageCircle className="w-5 h-5 mr-2" />
                  Falar no WhatsApp
                </Button>
                <Button
                  onClick={handleAcceptProposal}
                  size="lg"
                  className="bg-lime-400 hover:bg-lime-500 text-black font-bold text-lg px-8 py-6 shadow-lg shadow-lime-400/20"
                >
                  Aceitar Proposta
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
              {!selectedPlan && (
                <p className="text-zinc-500 text-sm mt-4">
                  Dica: Clique em um plano acima para selecioná-lo antes de aceitar
                </p>
              )}
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-black border-t border-zinc-800 py-12">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left">
                <div>
                  <h3 className="text-lime-400 font-bold text-lg mb-2">
                    {proposal.brandName || 'Sua Marca'}
                  </h3>
                  <p className="text-zinc-400 text-sm">{proposal.brandDescription}</p>
                </div>
                <div>
                  <h4 className="text-white font-semibold mb-2">Contato</h4>
                  <p className="text-zinc-400 text-sm">{proposal.contactEmail}</p>
                  <p className="text-zinc-400 text-sm">{proposal.contactPhone}</p>
                </div>
                <div>
                  <h4 className="text-white font-semibold mb-2">Redes Sociais</h4>
                  <p className="text-zinc-400 text-sm">{proposal.contactInstagram}</p>
                  <p className="text-zinc-400 text-sm">{proposal.contactWhatsApp}</p>
                </div>
              </div>
              <div className="border-t border-zinc-800 mt-8 pt-8 text-center">
                <p className="text-zinc-500 text-sm">
                  © {new Date().getFullYear()} {proposal.brandName || 'Sua Marca'}. Todos os direitos reservados.
                </p>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}