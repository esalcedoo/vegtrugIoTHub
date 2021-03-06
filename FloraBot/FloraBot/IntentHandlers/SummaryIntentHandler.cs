﻿using FloraBot.Dialogs;
using FloraBot.IntentHandlers;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Builder.Dialogs;
using Microsoft.Bot.Schema;
using System.Threading;
using System.Threading.Tasks;

namespace FloraBot.Services.LUIS
{
    public class SummaryIntentHandler : LUISIntentHandler
    {
        private readonly ConversationState _conversationState;
        private readonly SummaryDialog _summaryDialog;

        public SummaryIntentHandler(ConversationState conversationState, SummaryDialog resumeDialog)
        {
            _conversationState = conversationState;
            _summaryDialog = resumeDialog;
        }

        public override async Task<DialogTurnResult> Handle(DialogContext dialogContext, CancellationToken cancellationToken)
        {
            return await dialogContext.BeginDialogAsync(_summaryDialog.Id, cancellationToken: cancellationToken);
        }

        public override async Task Handle(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            await _summaryDialog.RunAsync(turnContext,
                            _conversationState.CreateProperty<DialogState>(nameof(DialogState)), cancellationToken);
        }

        public override bool IsValid(ITurnContext turnContext)
        {
            return GetTopIntentKey(turnContext) == "Summary";
        }
    }
}
