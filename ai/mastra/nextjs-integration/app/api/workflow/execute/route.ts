import { NextResponse, type NextRequest } from "next/server";
import { mastra } from "@src/mastra";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { query, owner, repo } = body;

    if (!query || !owner || !repo) {
      return NextResponse.json(
        {
          error: "Missing required parameters: query, owner, repo",
        },
        { status: 400 },
      );
    }

    const workflow = mastra.getWorkflow("handsonWorkflow");
    if (!workflow) {
      throw new Error("Workflow not found");
    }

    const run = await workflow.createRunAsync();
    const result = await run.start({
      inputData: {
        query,
        owner,
        repo,
      },
    });

    let message: string;
    let isSuccess: boolean;

    if (result.status === "success" && result.result.success) {
      message = "ワークフローが正常に完了しました";
      isSuccess = true;
    } else {
      message = "ワークフローの実行中にエラーが発生しました";
      isSuccess = false;
    }

    const workflowOutput = result.status === "success" ? result.result : null;
    const createdIssues = workflowOutput?.createdIssues || [];

    return NextResponse.json({
      success: isSuccess,
      confluencePages: [
        {
          title: query,
          message: "done",
        },
      ],
      githubIssues: createdIssues,
      message: message,
      steps: result.steps
        ? Object.keys(result.steps).map((stepId) => ({
            stepId,
            status: (result.steps as any)[stepId].status,
          }))
        : [],
    });
  } catch (error) {
    return NextResponse.json(
      {
        error: "error while executing workflow: ",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    );
  }
}
