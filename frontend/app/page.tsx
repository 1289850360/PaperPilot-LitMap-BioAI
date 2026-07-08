"use client";

import {
  BookOpen,
  ChevronLeft,
  ChevronRight,
  FileText,
  Folder,
  Languages,
  Loader2,
  MessageSquare,
  RefreshCcw,
  Save,
  Search,
  Table,
  Trash2,
  Upload,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { CompareTable } from "../components/CompareTable";
import { PaperCard } from "../components/PaperCard";
import {
  askPaper,
  deletePaper,
  DuplicatePaperError,
  fetchPapers,
  getPaperPageImageUrl,
  reextractPaper,
  updatePaperCardField,
  updatePaperFolder,
  uploadPaper,
} from "../lib/api";
import { DEFAULT_QUESTIONS, LANGUAGE_LABELS, type Language, TEXT } from "../lib/i18n";
import {
  buildPaperMarkdown,
  buildPapersCsv,
  downloadTextFile,
  safeExportName,
} from "../lib/exporters";
import type { AskResponse, FieldStatus, PaperFieldKey, PaperSummary } from "../lib/types";

const UNCATEGORIZED_FOLDER = "Uncategorized";
type AppView = "reader" | "compare";

export default function Home() {
  const [language, setLanguage] = useState<Language>("zh");
  const [activeView, setActiveView] = useState<AppView>("reader");
  const [papers, setPapers] = useState<PaperSummary[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [selectedCompareIds, setSelectedCompareIds] = useState<number[]>([]);
  const [question, setQuestion] = useState(DEFAULT_QUESTIONS.zh);
  const [answer, setAnswer] = useState<AskResponse | null>(null);
  const [folderDraft, setFolderDraft] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [pdfPage, setPdfPage] = useState(1);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const t = TEXT[language];

  const selectedPaper = useMemo(
    () => papers.find((paper) => paper.id === selectedId) ?? papers[0],
    [papers, selectedId],
  );

  const pageCount = selectedPaper?.page_count ?? 1;

  const selectedCompareIdSet = useMemo(
    () => new Set(selectedCompareIds),
    [selectedCompareIds],
  );

  const papersForCompare = useMemo(() => {
    if (!selectedCompareIds.length) return papers;
    return papers.filter((paper) => selectedCompareIdSet.has(paper.id));
  }, [papers, selectedCompareIds.length, selectedCompareIdSet]);

  const filteredPapers = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    if (!query) return papers;
    return papers.filter((paper) => paperSearchText(paper).includes(query));
  }, [papers, searchQuery]);

  const groupedPapers = useMemo(() => {
    const groups = new Map<string, PaperSummary[]>();
    for (const paper of filteredPapers) {
      const folder = paper.folder?.trim() || UNCATEGORIZED_FOLDER;
      groups.set(folder, [...(groups.get(folder) ?? []), paper]);
    }
    return Array.from(groups.entries()).map(([folder, items]) => ({ folder, items }));
  }, [filteredPapers]);

  useEffect(() => {
    const savedLanguage = window.localStorage.getItem("paperpilot-language");
    if (savedLanguage === "zh" || savedLanguage === "en") {
      setLanguage(savedLanguage);
      setQuestion(DEFAULT_QUESTIONS[savedLanguage]);
    }
  }, []);

  useEffect(() => {
    const folder = selectedPaper?.folder ?? UNCATEGORIZED_FOLDER;
    setFolderDraft(folder === UNCATEGORIZED_FOLDER ? "" : folder);
    setPdfPage(1);
  }, [selectedPaper?.id, selectedPaper?.folder]);

  useEffect(() => {
    fetchPapers()
      .then((items) => {
        setPapers(items);
        setSelectedId(items[0]?.id ?? null);
      })
      .catch(() => setError(t.backendNotReady));
  }, [t.backendNotReady]);

  function switchLanguage(nextLanguage: Language) {
    setLanguage(nextLanguage);
    window.localStorage.setItem("paperpilot-language", nextLanguage);
    if (question === DEFAULT_QUESTIONS.zh || question === DEFAULT_QUESTIONS.en) {
      setQuestion(DEFAULT_QUESTIONS[nextLanguage]);
    }
  }

  function displayFolder(folder: string) {
    return folder === UNCATEGORIZED_FOLDER ? t.uncategorized : folder;
  }

  function citationLabel(section: string, pageStart: number, pageEnd: number) {
    const pageRange = pageEnd !== pageStart ? `${pageStart}-${pageEnd}` : `${pageStart}`;
    if (language === "zh") {
      return `第 ${pageRange} 页，${section}`;
    }
    return `p. ${pageRange}, ${section}`;
  }

  function openPdfPage(page: number) {
    const maxPage = selectedPaper?.page_count ?? 1;
    setPdfPage(Math.min(Math.max(1, page), maxPage));
  }

  function nextPdfPage() {
    openPdfPage(pdfPage + 1);
  }

  function previousPdfPage() {
    openPdfPage(pdfPage - 1);
  }

  function toggleCompareSelection(paperId: number) {
    setSelectedCompareIds((ids) =>
      ids.includes(paperId) ? ids.filter((id) => id !== paperId) : [...ids, paperId],
    );
  }

  function clearCompareSelection() {
    setSelectedCompareIds([]);
  }

  function compareSelectionLabel() {
    if (!selectedCompareIds.length) return t.compareShowingAll;
    return t.compareSelectedCount.replace("{count}", String(selectedCompareIds.length));
  }

  function duplicateConfirmMessage(error: DuplicatePaperError) {
    const candidates = error.duplicates
      .map((paper) => `${paper.title} (${paper.filename})`)
      .join("\n");
    return candidates ? `${t.duplicateConfirm}\n\n${candidates}` : t.duplicateConfirm;
  }

  function exportCurrentPaperMarkdown() {
    if (!selectedPaper) return;
    const markdown = buildPaperMarkdown(selectedPaper, {
      fields: t.fields,
      statusLabels: t.statusLabels,
      verificationLabels: t.verificationLabels,
      uncategorized: t.uncategorized,
    });
    downloadTextFile(
      `${safeExportName(selectedPaper.title)}.md`,
      markdown,
      "text/markdown;charset=utf-8",
    );
  }

  function exportAllPapersCsv() {
    const csv = buildPapersCsv(papers, {
      fields: t.fields,
      statusLabels: t.statusLabels,
      verificationLabels: t.verificationLabels,
      uncategorized: t.uncategorized,
    });
    downloadTextFile("paperpilot-annotations.csv", csv, "text/csv;charset=utf-8");
  }

  async function onUpload(file: File | undefined) {
    if (!file) return;
    setBusy(true);
    setError("");
    setAnswer(null);
    try {
      const paper = await uploadPaper(file);
      setPapers((items) => [paper, ...items]);
      setSelectedId(paper.id);
    } catch (err) {
      if (err instanceof DuplicatePaperError && window.confirm(duplicateConfirmMessage(err))) {
        try {
          const paper = await uploadPaper(file, true);
          setPapers((items) => [paper, ...items]);
          setSelectedId(paper.id);
          return;
        } catch (forceErr) {
          setError(forceErr instanceof Error ? forceErr.message : t.uploadFailed);
          return;
        }
      }
      setError(err instanceof Error ? err.message : t.uploadFailed);
    } finally {
      setBusy(false);
    }
  }

  async function onSaveFolder() {
    if (!selectedPaper) return;
    setBusy(true);
    setError("");
    try {
      const updated = await updatePaperFolder(selectedPaper.id, folderDraft);
      setPapers((items) => items.map((paper) => (paper.id === updated.id ? updated : paper)));
    } catch {
      setError(t.uploadFailed);
    } finally {
      setBusy(false);
    }
  }

  async function onSaveCardField(
    field: PaperFieldKey,
    values: string[],
    status: FieldStatus,
  ) {
    if (!selectedPaper) return;
    setError("");
    try {
      const updated = await updatePaperCardField(selectedPaper.id, field, values, status);
      setPapers((items) => items.map((paper) => (paper.id === updated.id ? updated : paper)));
    } catch {
      setError(t.fieldUpdateFailed);
    }
  }

  async function onReextractPaper() {
    if (!selectedPaper) return;
    setBusy(true);
    setError("");
    setAnswer(null);
    try {
      const updated = await reextractPaper(selectedPaper.id);
      setPapers((items) => items.map((paper) => (paper.id === updated.id ? updated : paper)));
    } catch {
      setError(t.reextractFailed);
    } finally {
      setBusy(false);
    }
  }

  async function onDeletePaper(paper: PaperSummary) {
    if (!window.confirm(t.deleteConfirm)) return;
    setBusy(true);
    setError("");
    try {
      await deletePaper(paper.id);
      const remaining = papers.filter((item) => item.id !== paper.id);
      setPapers(remaining);
      setSelectedCompareIds((ids) => ids.filter((id) => id !== paper.id));
      if (selectedPaper?.id === paper.id) {
        setSelectedId(remaining[0]?.id ?? null);
        setAnswer(null);
      }
    } catch {
      setError(t.deleteFailed);
    } finally {
      setBusy(false);
    }
  }

  async function onAsk() {
    if (!selectedPaper || !question.trim()) return;
    setBusy(true);
    setError("");
    try {
      setAnswer(await askPaper(selectedPaper.id, question));
    } catch {
      setError(t.askFailed);
    } finally {
      setBusy(false);
    }
  }

  function openPaperFromCompare(paperId: number) {
    setSelectedId(paperId);
    setAnswer(null);
    setActiveView("reader");
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">LitMap-BioAI</p>
          <h1>PaperPilot</h1>
        </div>
        <div className="topbar-actions">
          <div className="language-toggle" aria-label="Language switcher">
            <Languages size={18} />
            {(["zh", "en"] as Language[]).map((item) => (
              <button
                aria-pressed={language === item}
                className={language === item ? "active" : ""}
                key={item}
                onClick={() => switchLanguage(item)}
                type="button"
              >
                {LANGUAGE_LABELS[item]}
              </button>
            ))}
          </div>
          <button
            className="secondary-action-button"
            disabled={!papers.length}
            onClick={exportAllPapersCsv}
            title={t.exportAllPapers}
            type="button"
          >
            <Table size={18} />
            <span>{t.exportCsv}</span>
          </button>
          <label className="upload-button">
            {busy ? <Loader2 className="spin" size={18} /> : <Upload size={18} />}
            <span>{t.uploadPdf}</span>
            <input
              type="file"
              accept="application/pdf"
              onChange={(event) => onUpload(event.target.files?.[0])}
            />
          </label>
        </div>
      </header>

      {error ? <div className="error">{error}</div> : null}

      <nav className="view-tabs" aria-label="PaperPilot views">
        <button
          className={activeView === "reader" ? "active" : ""}
          onClick={() => setActiveView("reader")}
          type="button"
        >
          <BookOpen size={18} />
          <span>{t.readerView}</span>
        </button>
        <button
          className={activeView === "compare" ? "active" : ""}
          onClick={() => setActiveView("compare")}
          type="button"
        >
          <Table size={18} />
          <span>{t.compareView}</span>
        </button>
      </nav>

      {activeView === "compare" ? (
        <section className="compare-shell">
          <div className="compare-selection-bar">
            <span>{compareSelectionLabel()}</span>
            {selectedCompareIds.length ? (
              <button onClick={clearCompareSelection} type="button">
                {t.clearCompareSelection}
              </button>
            ) : null}
          </div>
          <CompareTable
            papers={papersForCompare}
            fieldLabels={t.fields}
            statusLabels={t.statusLabels}
            verificationLabels={t.verificationLabels}
            emptyLabel={t.notFound}
            searchPlaceholder={t.compareSearch}
            titleLabel={t.compareTitle}
            hintLabel={t.compareHint}
            openLabel={t.openReader}
            noResultsLabel={t.noSearchResults}
            titleHeader={t.titleHeader}
            folderHeader={t.folderHeader}
            statusHeader={t.statusHeader}
            uncategorizedLabel={t.uncategorized}
            onOpenPaper={openPaperFromCompare}
          />
        </section>
      ) : (
      <section className="workspace">
        <aside className="sidebar">
          <div className="panel-title">
            <FileText size={18} />
            <span>{t.papers}</span>
          </div>
          <div className="search-box">
            <Search size={16} />
            <input
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              placeholder={t.search}
            />
          </div>
          {papers.length ? (
            groupedPapers.length ? (
              groupedPapers.map((group) => (
                <section className="folder-group" key={group.folder}>
                  <div className="folder-heading">
                    <Folder size={15} />
                    <span>{displayFolder(group.folder)}</span>
                  </div>
                  {group.items.map((paper) => (
                    <div
                      className={paper.id === selectedPaper?.id ? "paper-tab active" : "paper-tab"}
                      key={paper.id}
                    >
                      <label className="compare-check" title={t.selectForCompare}>
                        <input
                          aria-label={`${t.selectForCompare}: ${paper.title}`}
                          checked={selectedCompareIdSet.has(paper.id)}
                          onChange={() => toggleCompareSelection(paper.id)}
                          type="checkbox"
                        />
                      </label>
                      <button
                        className="paper-select"
                        onClick={() => {
                          setSelectedId(paper.id);
                          setAnswer(null);
                        }}
                        type="button"
                      >
                        <span>{paper.title}</span>
                        <small>{paper.filename}</small>
                      </button>
                      <button
                        aria-label={t.deletePaper}
                        className="delete-paper-button"
                        disabled={busy}
                        onClick={() => onDeletePaper(paper)}
                        title={t.deletePaper}
                        type="button"
                      >
                        <Trash2 size={15} />
                      </button>
                    </div>
                  ))}
                </section>
              ))
            ) : (
              <p className="hint">{t.noSearchResults}</p>
            )
          ) : (
            <p className="hint">{t.emptySidebar}</p>
          )}
        </aside>

        <section className="content">
          {selectedPaper ? (
            <>
              <section className="folder-panel">
                <div className="panel-title-row">
                  <div className="panel-title">
                    <Folder size={18} />
                    <span>{t.folder}</span>
                  </div>
                  <div className="panel-actions">
                    <button
                      className="secondary-action-button"
                      disabled={busy}
                      onClick={onReextractPaper}
                      title={t.reextractPaper}
                      type="button"
                    >
                      {busy ? <Loader2 className="spin" size={18} /> : <RefreshCcw size={18} />}
                      <span>{t.reextractPaper}</span>
                    </button>
                    <button
                      className="secondary-action-button"
                      onClick={exportCurrentPaperMarkdown}
                      title={t.exportCurrentPaper}
                      type="button"
                    >
                      <FileText size={18} />
                      <span>{t.exportMarkdown}</span>
                    </button>
                  </div>
                </div>
                <div className="folder-row">
                  <input
                    value={folderDraft}
                    onChange={(event) => setFolderDraft(event.target.value)}
                    placeholder={t.folderPlaceholder}
                  />
                  <button onClick={onSaveFolder} disabled={busy} type="button">
                    {busy ? <Loader2 className="spin" size={18} /> : <Save size={18} />}
                    <span>{t.saveFolder}</span>
                  </button>
                </div>
              </section>
              <section className="pdf-panel">
                <div className="pdf-panel-header">
                  <div>
                    <div className="panel-title">
                      <FileText size={18} />
                      <span>{t.pdfPreview}</span>
                    </div>
                    <p>{t.pdfPreviewHint}</p>
                  </div>
                  <label className="page-control">
                    <span>{t.page}</span>
                    <input
                      min={1}
                      onChange={(event) => openPdfPage(Number(event.target.value) || 1)}
                      type="number"
                      value={pdfPage}
                    />
                  </label>
                </div>
                <div className="pdf-frame">
                  <div className="pdf-scroll-area">
                    <img
                      alt={`${selectedPaper.title} page ${pdfPage}`}
                      key={`${selectedPaper.id}-${pdfPage}`}
                      src={getPaperPageImageUrl(selectedPaper.id, pdfPage)}
                    />
                  </div>
                  <div className="page-turner" aria-label="PDF page navigation">
                    <button
                      aria-label="Previous page"
                      disabled={pdfPage <= 1}
                      onClick={previousPdfPage}
                      type="button"
                    >
                      <ChevronLeft size={22} />
                    </button>
                    <span>
                      {pdfPage}/{pageCount}
                    </span>
                    <button
                      aria-label="Next page"
                      disabled={pdfPage >= pageCount}
                      onClick={nextPdfPage}
                      type="button"
                    >
                      <ChevronRight size={22} />
                    </button>
                  </div>
                </div>
              </section>
              <PaperCard
                paper={selectedPaper}
                fieldLabels={t.fields}
                emptyLabel={t.notFound}
                evidenceLabel={t.evidence}
                hideEvidenceLabel={t.hideEvidence}
                citationLabel={citationLabel}
                openPageLabel={t.openPage}
                editLabel={t.edit}
                cancelLabel={t.cancel}
                saveLabel={t.save}
                oneItemPerLineLabel={t.oneItemPerLine}
                statusLabels={t.statusLabels}
                verificationLabels={t.verificationLabels}
                onOpenPage={openPdfPage}
                onSaveField={onSaveCardField}
              />
              <section className="qa-panel">
                <div className="panel-title">
                  <MessageSquare size={18} />
                  <span>{t.citationQa}</span>
                </div>
                <div className="ask-row">
                  <input
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    placeholder={t.questionPlaceholder}
                  />
                  <button onClick={onAsk} disabled={busy}>
                    {busy ? <Loader2 className="spin" size={18} /> : t.ask}
                  </button>
                </div>
                {answer ? (
                  <div className="answer">
                    <p>{answer.answer}</p>
                    <div className="citations">
                      {answer.citations.map((citation, index) => (
                        <blockquote key={`${citation.page_start}-${index}`}>
                          <button
                            className="citation-jump-button"
                            onClick={() => openPdfPage(citation.page_start)}
                            title={t.openPage}
                            type="button"
                          >
                            {citationLabel(citation.section, citation.page_start, citation.page_end)}
                          </button>
                          <span>{citation.text}</span>
                        </blockquote>
                      ))}
                    </div>
                  </div>
                ) : null}
              </section>
            </>
          ) : (
            <section className="empty-state">
              <FileText size={40} />
              <h2>{t.noPapersTitle}</h2>
              <p>{t.noPapersBody}</p>
            </section>
          )}
        </section>
      </section>
      )}
    </main>
  );
}

function paperSearchText(paper: PaperSummary) {
  const fields = [
    paper.title,
    paper.filename,
    paper.folder,
    paper.abstract ?? "",
    ...paper.card.task,
    ...paper.card.datasets,
    ...paper.card.models_or_methods,
    ...paper.card.baselines,
    ...paper.card.metrics,
    ...paper.card.main_result,
    ...paper.card.limitations,
    ...paper.card.code_availability,
  ];
  return fields.join(" ").toLowerCase();
}
