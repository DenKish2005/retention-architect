using Retention.Api.Extensions;
using Retention.Api.Models.Config;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<MlServiceOptions>(
    builder.Configuration.GetSection("MlService"));

builder.Services.AddApplicationServices();

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

await app.RunAsync();