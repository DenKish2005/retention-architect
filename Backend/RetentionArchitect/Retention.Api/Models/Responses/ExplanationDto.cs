namespace Retention.Api.Models.Responses;

public class ExplanationDto
{
    public string Feature { get; set; } = string.Empty;
    public double Impact { get; set; }
    public string Direction { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
}